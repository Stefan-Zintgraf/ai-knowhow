# Security Scan Report - Claude Code Training Exercise Projects

**Date:** June 27, 2025  
**Scan Focus:** SQL Injection, XSS, Authentication/Authorization, Input Validation, Cryptography, Hardcoded Credentials

## Executive Summary

This security scan has identified **CRITICAL** vulnerabilities across all exercise projects. These vulnerabilities appear to be intentionally placed for educational purposes, demonstrating common security anti-patterns in each technology stack.

## Critical Findings by Project

### 1. Python - Weather App (Flask)

#### Severity: LOW-MEDIUM

**Findings:**
- **Hardcoded API Key Pattern** (Line 12): The app uses environment variables correctly but has commented code showing direct API key usage
- **Debug Mode Enabled** (Line 97): `app.run(debug=True)` exposes detailed error information in production
- **No Input Sanitization**: User input from city names is passed directly to external API without validation
- **HTTP Protocol in API Call** (Line 11): GEOCODING_API_ENDPOINT uses HTTP instead of HTTPS
- **Potential Path Traversal in Templates**: Image sources constructed using `{{ current_weather.lower() }}.png` without validation

**Recommendations:**
- Disable debug mode in production
- Validate city input against allowed characters
- Use HTTPS for all API endpoints
- Sanitize weather type values before using in image paths

### 2. Python - Flask API

#### Severity: CRITICAL

**Findings:**

1. **SQL Injection Vulnerabilities** (CRITICAL):
   - `database.py` lines 24, 67, 81, 122, 136: Direct string concatenation in SQL queries
   ```python
   _c.execute("SELECT pw FROM users WHERE id = '" + id + "';")  # Line 24
   command = "SELECT note_id, timestamp, note FROM notes WHERE user = '" + id.upper() + "';"  # Line 67
   ```

2. **Hardcoded Secret Key** (CRITICAL):
   - `config.py` line 1: `SECRET_KEY = "fdsafasd"` - Weak, hardcoded session secret

3. **Authentication Bypass Vulnerabilities**:
   - No password complexity requirements
   - Plain text password comparison after hashing
   - Session management issues

4. **Input Validation Issues**:
   - Lines 187-192 in `app.py`: Weak validation only checks for spaces and single quotes
   - No proper sanitization of user inputs

5. **Path Traversal Risk**:
   - File operations without proper path validation

6. **Information Disclosure**:
   - Debug mode enabled (Line 204)
   - Detailed error pages expose system information

**Recommendations:**
- Use parameterized queries for ALL database operations
- Generate secure random secret keys and store in environment variables
- Implement proper input validation and sanitization
- Add authentication rate limiting
- Disable debug mode in production

### 3. JavaScript - Lyrics Trainer (TypeScript)

#### Severity: LOW

**Findings:**

1. **Client-Side Security** (LOW):
   - All security logic is client-side and can be bypassed
   - No server-side validation of uploaded files

2. **Local Storage Security**:
   - Sensitive data stored in localStorage without encryption
   - No integrity checks on stored data

3. **File Upload Risks**:
   - No file size limits enforced
   - Minimal file type validation (only checks extension)
   - Potential for malicious file content

4. **XSS Potential**:
   - Line 362: `els.box.textContent = lyrics[state.idx];` - Uses textContent (safe)
   - However, file names displayed without proper escaping in some places

**Recommendations:**
- Implement server-side validation for file uploads
- Add file size limits
- Sanitize file names before display
- Consider content security policy headers

### 4. Java - Certificate Service (Spring Boot)

#### Severity: MEDIUM

**Findings:**

1. **Authentication/Authorization**:
   - No authentication implemented for certificate generation endpoint
   - Anyone can generate certificates without verification

2. **Input Validation**:
   - Book title validation exists but could be bypassed
   - No rate limiting on certificate generation

3. **Sensitive Data Exposure**:
   - Certificate ID exposed in headers
   - Keystore path potentially exposed in error messages

4. **Database Security**:
   - H2 console enabled (line 20-21 in application.yaml)
   - Default credentials for H2 database

5. **Path Traversal**:
   - Certificate filename in URL path (line 164) could be exploited

**Recommendations:**
- Implement authentication for certificate generation
- Add rate limiting to prevent abuse
- Disable H2 console in production
- Validate and sanitize file paths
- Use secure random certificate IDs

### 5. Java - Shopping Service (Grails/Groovy)

#### Severity: HIGH

**Findings:**

1. **SQL Logging Enabled** (HIGH):
   - `DataSource.groovy` lines 8-9: SQL queries logged in plain text
   ```groovy
   logSql = true
   formatSql = true
   ```

2. **Default Credentials**:
   - H2 database uses default credentials (sa/empty password)

3. **No Input Validation**:
   - Controllers accept params directly without validation
   - `Customer.list(params)` passes user input directly to database

4. **Mass Assignment Vulnerability**:
   - Scaffold controllers allow all parameters to be set

5. **XSS Vulnerabilities**:
   - Default codec is HTML but some outputs use 'none' encoding
   - Line 54: `taglib = 'none'` disables escaping

6. **Information Disclosure**:
   - Detailed error information exposed
   - Stack traces visible to users

**Recommendations:**
- Disable SQL logging in production
- Change default database credentials
- Implement input validation
- Use parameter binding
- Enable proper output encoding
- Configure custom error pages

## Common Anti-Patterns Across Projects

1. **Debug Mode in Production**: All projects have debug/development settings enabled
2. **Weak Secrets Management**: Hardcoded credentials and weak secret keys
3. **Insufficient Input Validation**: Most projects lack proper input sanitization
4. **Missing Authentication**: Limited or no authentication mechanisms
5. **Information Disclosure**: Detailed error messages expose system internals

## Risk Matrix

| Project | SQL Injection | XSS | Auth Issues | Input Validation | Crypto | Hardcoded Creds | Overall Risk |
|---------|--------------|-----|-------------|------------------|--------|-----------------|--------------|
| Weather App | N/A | Low | N/A | Medium | N/A | Low | LOW-MEDIUM |
| Flask API | CRITICAL | Medium | High | High | Low | CRITICAL | CRITICAL |
| Lyrics Trainer | N/A | Low | N/A | Medium | N/A | N/A | LOW |
| Certificate Service | Low | Low | High | Medium | Medium | Medium | MEDIUM |
| Shopping Service | High | High | Medium | High | N/A | High | HIGH |

## Immediate Actions Required

1. **Flask API**: Fix SQL injection vulnerabilities immediately
2. **Shopping Service**: Disable SQL logging and fix XSS vulnerabilities
3. **All Projects**: Disable debug modes and implement proper error handling
4. **All Projects**: Implement proper input validation and sanitization
5. **All Projects**: Move secrets to environment variables

## Educational Value

These vulnerabilities provide excellent examples of common security mistakes in each technology stack:
- Python/Flask: SQL injection, weak session management
- JavaScript: Client-side security limitations, file upload risks
- Java/Spring Boot: Authentication gaps, configuration security
- Groovy/Grails: Mass assignment, output encoding issues

The projects effectively demonstrate why security must be considered at every layer of the application stack.