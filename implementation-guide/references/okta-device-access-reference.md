# Okta Device Access Reference

## Platform Components

Use these component names consistently across all documents. Map use cases to the appropriate components.

### Core Device Access Components

| Component | What It Does | Common Use Cases |
|-----------|-------------|------------------|
| **Okta Device Access (ODA)** | Umbrella term for extending Okta authentication to OS login on managed Windows and macOS devices | All device-login use cases |
| **Desktop MFA for Windows** | Enforces Okta MFA at the Windows sign-in screen, lock screen, and privilege elevation prompts | Compliance-driven MFA at login, cyber insurance requirements, shared/kiosk device hardening |
| **Desktop MFA for macOS** | Links a user's local macOS account to their Okta identity and enforces MFA at macOS login | Same as Windows, for Mac fleets |
| **Desktop Password Sync (macOS)** | Syncs the macOS local account password with the Okta password via Apple Platform SSO | Single-credential experience on Mac, reducing password reset volume |
| **Okta Verify (desktop)** | The client agent installed on the Windows/macOS device; performs push, TOTP, biometric, and FastPass challenges at OS login | Required agent for Desktop MFA, offline OTP, and FastPass at OS login |
| **Okta FastPass at OS login** | Phishing-resistant, passwordless authentication at the device login screen, using Windows Hello or Touch ID as the local user-verification factor | Passwordless desktop login, reducing prompt fatigue, phishing resistance at the endpoint |
| **Offline MFA / Offline OTP** | Okta Verify-generated time-based passcodes usable when the device has no network connectivity | Field workers, air-gapped environments, intermittent connectivity |
| **Device Access certificates (SCEP)** | Certificates deployed via MDM/SCEP that identify the device to specific Device Access API endpoints | Establishing device identity for Device Access API calls (separate from device trust/assurance certificates) |
| **Desktop Password Autofill** | Autofills the Okta password at the sign-in screen after primary authentication | Reducing friction for password-based fallback flows |

### Supporting Components

| Component | What It Does |
|-----------|-------------|
| **WIC Sign-On Policies / Authenticators** | The underlying Workforce Identity Cloud policy engine that defines which factors are allowed; Device Access enforces these policies at the OS layer instead of just the app layer |
| **MDM (Microsoft Intune, Jamf, Workspace ONE, SCCM/GPO)** | Required third-party tool to deploy the Okta Verify installer, configuration profiles, and (for macOS) the Platform SSO extensible payload — Okta does not provide its own MDM |
| **Active Directory / Microsoft Entra ID** | Windows devices must be domain- or Entra-joined; Desktop MFA integrates with the existing directory join, it does not replace it |
| **Apple Platform SSO** | Apple's native framework that Desktop Password Sync (and passwordless macOS login) is built on top of |
| **Device Trust / Device Assurance policies** | Separate WIC capability that evaluates device posture (OS version, encryption, screen lock) as a sign-in condition; Device Access certificates are explicitly distinct from device assurance certificates |

### Important Distinctions

**Desktop MFA vs app-level MFA**
- App-level MFA (standard WIC Sign-On Policy) challenges a user when they authenticate to an app or the Okta dashboard.
- Desktop MFA moves that challenge to the OS login screen itself — before the user ever reaches a browser or app. It requires the Okta Verify desktop agent; app-level MFA does not.
- Don't assume enabling WIC MFA policies automatically secures the Windows/macOS login screen — Desktop MFA is a separate deployment (installer + MDM configuration profile) on top of the policy.

**Device Access vs Device Trust / Device Assurance**
- Device Access is about authenticating the *user* at the OS login prompt (Desktop MFA, Desktop Password Sync, FastPass at OS login).
- Device Trust / Device Assurance is about evaluating the *device's* security posture as a condition inside a WIC Sign-On Policy (e.g., "require FileVault enabled").
- Device Access certificates (SCEP) are explicitly documented as separate from the certificates used for managed device attestation — don't conflate the two certificate types when scoping a project.
- Reference the organization's WIC reference material for Sign-On Policy and device assurance detail; this file does not duplicate that content.

**Online vs offline factors**
- Online authenticators for Desktop MFA: Okta Verify Push, Okta Verify TOTP, RSA SecurID token, FIDO2 security keys.
- Offline authenticators: Okta Verify TOTP, OATH-compliant security keys, and (Windows only) Windows Hello biometrics.
- Offline OTP is a fallback path, not a full parity experience — plan enrollment (QR code scan into Okta Verify) before users go offline, not after.

**Desktop MFA vs FastPass at OS login**
- Desktop MFA is the general capability name (any supported factor at the login screen).
- FastPass at OS login is specifically the phishing-resistant, passwordless path, using local biometrics/PIN (Windows Hello, Touch ID) as the user-verification step. It requires Okta Verify with FastPass support and is not automatically the same as "Desktop MFA is configured."

---

## Common Device Access Use Case Patterns

### MFA at Windows/macOS OS Login

**Typical flow:**
Device joined to AD/Entra (Windows) or enrolled in MDM (macOS) → Okta Verify installed via MDM → Desktop MFA policy applied → User enters username/password at OS login → Okta Verify challenge (push/TOTP/security key) → Login granted → Device account unlocked

**Key Okta components:** Desktop MFA (Windows or macOS), Okta Verify (desktop), MDM deployment, underlying WIC Sign-On Policy

**Discovery questions:**
- Are target devices already Active Directory- or Microsoft Entra-joined (Windows) or MDM-enrolled (macOS)? Desktop MFA cannot be deployed without this.
- What MDM is in place to push the Okta Verify installer and configuration profiles (Intune, Jamf, Workspace ONE, SCCM/GPO)?
- Is Remote Desktop Protocol (RDP) access in scope? Desktop MFA for Windows does not support RDP sessions today — this needs a documented workaround or exception.
- What is the fallback experience if a user's device has no network connectivity at login?
- Are there shared/kiosk devices where per-user Desktop MFA doesn't map cleanly to a single local account?

### Offline MFA When Disconnected

**Typical flow:**
User enrolls offline OTP (QR code scanned into Okta Verify while online) → User goes offline → OS login prompts for offline passcode → User opens Okta Verify, reads TOTP code → Enters code at login → Login granted, reconciled with Okta once reconnected

**Key Okta components:** Offline MFA / Offline OTP, Okta Verify (desktop and/or mobile), Desktop MFA policy

**Discovery questions:**
- Which user populations regularly work without connectivity (field technicians, ships, remote sites, secure facilities)?
- Has offline enrollment been completed before the device goes offline? (It cannot be done after the fact.)
- Is Windows Hello biometrics an acceptable offline factor, or is a code-based OTP required for policy/compliance reasons?
- What is the process if a device is offline long enough that the local offline credential needs to be refreshed?
- Are helpdesk/support processes updated to handle offline-login lockouts, since standard password reset flows assume connectivity?

### Phishing-Resistant Login to the Endpoint (FastPass at OS Login)

**Typical flow:**
Okta Verify with FastPass enrolled on the device → User initiates OS login → FastPass challenge issued → Local biometric/PIN check (Windows Hello / Touch ID) satisfies possession + inherence → Device-bound key signs the challenge → Login granted without a password prompt

**Key Okta components:** Okta FastPass at OS login, Okta Verify (desktop), Device Access certificates, underlying WIC phishing-resistant authenticator policy

**Discovery questions:**
- Do target devices have the hardware to support Windows Hello or Touch ID (biometric sensor, TPM)?
- Is the goal full passwordless login, or FastPass as one option alongside a password/PIN fallback?
- Are there virtual desktop (VDI) users in scope? FastPass support in virtual Windows environments is a newer, more limited capability — validate current support against the specific VDI platform in use.
- What is the enrollment/re-enrollment process when a user gets a new device?
- Does the customer's compliance framework require this to be documented as satisfying phishing-resistant MFA specifically (vs. generic MFA)?

### Password Sync Between Okta and the Desktop

**Typical flow:**
Device enrolled in MDM with Platform SSO payload deployed → User's Okta password syncs to the local macOS account → Password policy changes in Okta (rotation, complexity) propagate to the local login password → User authenticates to macOS and Okta with one credential

**Key Okta components:** Desktop Password Sync (macOS only), Apple Platform SSO, MDM (Jamf/Intune/Workspace ONE)

**Discovery questions:**
- Is the fleet on macOS 14 Sonoma or later? Desktop Password Sync depends on Apple Platform SSO, which has a hard OS floor.
- Has macOS local password expiration been disabled at the MDM level before rollout, as Okta's own deployment guidance requires?
- Are there users with multiple local accounts on one Mac, or shared devices? Desktop Password Sync ties one Okta identity to one local account, and re-enrolling a second local account under the same Okta credentials requires a factory reset.
- Is this being requested as a stepping stone toward full passwordless (FastPass at OS login), or as a standalone password-management improvement?
- Is Windows password sync also expected? Desktop Password Sync as documented is macOS-specific — Windows password behavior needs to be scoped separately.

---

## Honest Capability Assessment

When creating implementation guides, be accurate about what Device Access can and cannot do natively. Do not overstate capabilities.

### Device Access Strengths (lean into these)
- Moves MFA and phishing-resistant authentication to the actual OS login prompt, not just the app/browser layer
- Reuses the existing Okta Verify agent and WIC authenticator policies rather than introducing a separate product
- Desktop Password Sync removes a real pain point (separate local Mac password) using Apple's native Platform SSO framework, not a custom Okta agent hack
- FastPass at OS login gives a genuine phishing-resistant, low-friction login path where hardware supports it
- Device Access certificates give a clean, purpose-built device-identity mechanism for API calls, kept separate from device assurance certificates

### Gaps to Acknowledge (document as discovery items, not limitations)
- **No Linux support**: Desktop MFA, Desktop Password Sync, and FastPass at OS login are Windows and macOS only. Linux endpoints need a separate, non-Okta-native answer — do not imply parity.
- **No RDP support (Windows)**: Desktop MFA for Windows explicitly does not cover Remote Desktop Protocol sessions. Any RDP-heavy environment needs a documented exception or compensating control.
- **MDM is a hard prerequisite, not optional**: Okta does not ship its own device management. Deployment depends entirely on a third-party MDM (Intune, Jamf, Workspace ONE, or GPO/SCCM for Windows) to push the Okta Verify installer and configuration profiles/payloads. No MDM in place means no Device Access rollout, full stop.
- **Desktop Password Sync has a real OS floor**: It requires macOS 14 Sonoma or later (via Apple Platform SSO). Older Mac fleets cannot use it regardless of Okta licensing.
- **Licensing is a separate add-on**: Device Access is sold as its own itemized product/add-on on top of a Workforce Identity Cloud suite, not a feature automatically included with WIC or standard MFA. Confirm the customer's contract includes it before scoping.
- **Offline is a fallback, not a full experience**: Offline OTP/biometrics require enrollment while still online, and the offline factor set is narrower than the online factor set (no push, no RSA SecurID). Plan for this explicitly rather than assuming seamless parity.
- **FastPass in VDI is still maturing**: FastPass support in virtual Windows environments is newer and more constrained than physical-device support — verify current state against the specific VDI platform rather than assuming general availability.
- **Local-account model constraints (macOS)**: Desktop Password Sync ties one Okta identity to one local macOS account; multiple local accounts or shared-Mac scenarios don't map cleanly and may require a factory reset to reassign.

Frame gaps as discovery items: "Validate whether [capability] meets the customer's specific device fleet and connectivity requirements, or if a compensating control/exception process is needed."

---

## Diagram Component Mapping

When creating Mermaid diagrams for Okta Device Access, use these class assignments:

| Okta Component | Mermaid Class |
|---------------|---------------|
| Device power-on, user-initiated login attempt | `trigger` |
| MDM (Intune, Jamf, Workspace ONE, SCCM/GPO), Active Directory, Microsoft Entra ID | `extSystem` |
| Okta Verify (desktop), Desktop MFA, Desktop Password Sync, FastPass at OS login | `platform` |
| Okta Workflows (custom remediation/notification logic, if used) | `workflow` |
| MFA challenge evaluation, online-vs-offline branch, FastPass verification check | `decision` |
| WIC Sign-On Policy enforcement, Device Assurance evaluation | `governance` |
| Local account provisioning, password sync to local account, certificate issuance (SCEP) | `action` |
| Device unlocked / user signed in | `endpoint` |
| Login denied, lockout after failed offline attempts | `danger` |
| Device Access certificate issuance log, sign-in event log | `audit` |
| Helpdesk/administrator alert on lockout or enrollment failure | `notify` |
