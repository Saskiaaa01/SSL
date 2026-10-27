import socket
import ssl
import ipaddress
import time
import hashlib
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, dsa, ec
from app.core.config import settings


def is_private_ip(hostname: str) -> bool:
    """SSRF Protection: Check if resolved hostname belongs to private/internal IP space."""
    try:
        ip_str = socket.gethostbyname(hostname)
        ip = ipaddress.ip_address(ip_str)
        return (
            ip.is_private
            or ip.is_loopback
            or ip.is_link_local
            or ip.is_multicast
            or ip.is_reserved
        )
    except Exception:
        return False


def match_hostname(pattern: str, hostname: str) -> bool:
    """Matches hostname against pattern with wildcard support (e.g., *.dinas.go.id)."""
    pattern = pattern.lower().strip()
    hostname = hostname.lower().strip()
    if pattern == hostname:
        return True
    if pattern.startswith("*."):
        suffix = pattern[1:]  # .dinas.go.id
        if hostname.endswith(suffix) and hostname.count(".") == pattern.count("."):
            return True
    return False


def inspect_ssl_certificate(domain: str, port: int = 443) -> Dict[str, Any]:
    """
    Inspects public SSL/TLS certificate for a domain:
    - Performs TLS handshake with SNI
    - Extracts validity, days remaining, SANs, issuer, fingerprint, serial, key info
    - Validates hostname matching and calculates status
    """
    clean_domain = domain.strip().lower()

    # SSRF Protection Check
    if settings.SSRF_PROTECTION_ENABLED and is_private_ip(clean_domain):
        return {
            "status": "FAILED",
            "days_remaining": None,
            "issuer": "Blocked (SSRF)",
            "subject_cn": clean_domain,
            "valid_from": "-",
            "expires_at": "-",
            "fingerprint_sha256": "-",
            "serial_number": "-",
            "key_info": "-",
            "sans": "-",
            "chain_valid": False,
            "hostname_match": False,
            "error_message": "Akses ditolak: Alamat IP privat/loopback diblokir oleh sistem SSRF Protection.",
            "response_time_ms": 0,
        }

    start_time = time.time()
    
    context = ssl.create_default_context()
    context.check_hostname = True
    context.verify_mode = ssl.CERT_REQUIRED

    try:
        with socket.create_connection((clean_domain, port), timeout=settings.SSL_SOCKET_TIMEOUT_SECONDS) as sock:
            with context.wrap_socket(sock, server_hostname=clean_domain) as ssock:
                response_time_ms = int((time.time() - start_time) * 1000)
                
                # Binary DER certificate for accurate cryptography parsing
                der_cert = ssock.getpeercert(binary_form=True)
                cert = x509.load_der_x509_certificate(der_cert, default_backend())

                # SHA-256 Fingerprint
                sha256_hash = hashlib.sha256(der_cert).hexdigest().upper()
                fingerprint = ":".join(sha256_hash[i:i+2] for i in range(0, len(sha256_hash), 2))

                # Serial Number (formatted in hex)
                serial_hex = format(cert.serial_number, "x")
                if len(serial_hex) % 2 != 0:
                    serial_hex = "0" + serial_hex
                serial_formatted = ":".join(serial_hex[i:i+2] for i in range(0, len(serial_hex), 2))

                # Subject CN
                subject_cn = clean_domain
                try:
                    cns = cert.subject.get_attributes_for_oid(x509.NameOID.COMMON_NAME)
                    if cns:
                        subject_cn = cns[0].value
                except Exception:
                    pass

                # Issuer Org / CN
                issuer = "Unknown Issuer"
                try:
                    issuer_orgs = cert.issuer.get_attributes_for_oid(x509.NameOID.ORGANIZATION_NAME)
                    issuer_cns = cert.issuer.get_attributes_for_oid(x509.NameOID.COMMON_NAME)
                    if issuer_orgs:
                        issuer = issuer_orgs[0].value
                    elif issuer_cns:
                        issuer = issuer_cns[0].value
                except Exception:
                    pass

                # SANs (Subject Alternative Names)
                sans_list: List[str] = []
                try:
                    ext = cert.extensions.get_extension_for_oid(x509.ExtensionOID.SUBJECT_ALTERNATIVE_NAME)
                    sans_list = ext.value.get_values_for_type(x509.DNSName)
                except Exception:
                    sans_list = [subject_cn]

                # Public Key Info
                key_info = "Unknown Key Type"
                pub_key = cert.public_key()
                if isinstance(pub_key, rsa.RSAPublicKey):
                    key_info = f"RSA {pub_key.key_size} bit (SHA256withRSA)"
                elif isinstance(pub_key, ec.EllipticCurvePublicKey):
                    key_info = f"ECDSA {pub_key.key_size} bit ({pub_key.curve.name})"
                elif isinstance(pub_key, dsa.DSAPublicKey):
                    key_info = f"DSA {pub_key.key_size} bit"

                # Validity dates
                valid_from_dt = cert.not_valid_before_utc if hasattr(cert, "not_valid_before_utc") else cert.not_valid_before.replace(tzinfo=timezone.utc)
                expires_at_dt = cert.not_valid_after_utc if hasattr(cert, "not_valid_after_utc") else cert.not_valid_after.replace(tzinfo=timezone.utc)
                now_dt = datetime.now(timezone.utc)

                days_remaining = (expires_at_dt - now_dt).days

                # Hostname Match Verification
                match = any(match_hostname(pattern, clean_domain) for pattern in [subject_cn] + sans_list)

                # Determine Status Code
                if days_remaining <= 0:
                    status = "EXPIRED"
                elif days_remaining <= 7:
                    status = "CRITICAL_7"
                elif days_remaining <= 14:
                    status = "WARNING_14"
                elif days_remaining <= 30:
                    status = "WARNING_30"
                else:
                    status = "VALID"

                return {
                    "status": status,
                    "days_remaining": days_remaining,
                    "issuer": issuer,
                    "subject_cn": subject_cn,
                    "valid_from": valid_from_dt.strftime("%Y-%m-%d"),
                    "expires_at": expires_at_dt.strftime("%Y-%m-%d"),
                    "fingerprint_sha256": fingerprint,
                    "serial_number": serial_formatted,
                    "key_info": key_info,
                    "sans": ", ".join(sans_list) if sans_list else subject_cn,
                    "chain_valid": True,
                    "hostname_match": match,
                    "error_message": None if match else "Hostname tidak cocok dengan Common Name atau SAN sertifikat.",
                    "response_time_ms": response_time_ms,
                }

    except ssl.SSLCertVerificationError as e:
        response_time_ms = int((time.time() - start_time) * 1000)
        return {
            "status": "FAILED",
            "days_remaining": None,
            "issuer": "Untrusted / Invalid Chain",
            "subject_cn": clean_domain,
            "valid_from": "-",
            "expires_at": "-",
            "fingerprint_sha256": "-",
            "serial_number": "-",
            "key_info": "-",
            "sans": "-",
            "chain_valid": False,
            "hostname_match": False,
            "error_message": f"SSL Handshake Gagal (Sertifikat Tidak Valid / Self-Signed): {str(e)}",
            "response_time_ms": response_time_ms,
        }
    except (socket.timeout, TimeoutError):
        return {
            "status": "FAILED",
            "days_remaining": None,
            "issuer": "Connection Timeout",
            "subject_cn": clean_domain,
            "valid_from": "-",
            "expires_at": "-",
            "fingerprint_sha256": "-",
            "serial_number": "-",
            "key_info": "-",
            "sans": "-",
            "chain_valid": False,
            "hostname_match": False,
            "error_message": "Batas waktu koneksi habis (Connection Timeout) pada port 443.",
            "response_time_ms": int((time.time() - start_time) * 1000),
        }
    except Exception as e:
        return {
            "status": "FAILED",
            "days_remaining": None,
            "issuer": "Tidak Diketahui",
            "subject_cn": clean_domain,
            "valid_from": "-",
            "expires_at": "-",
            "fingerprint_sha256": "-",
            "serial_number": "-",
            "key_info": "-",
            "sans": "-",
            "chain_valid": False,
            "hostname_match": False,
            "error_message": f"Koneksi gagal atau host tidak terjangkau: {str(e)}",
            "response_time_ms": int((time.time() - start_time) * 1000),
        }
