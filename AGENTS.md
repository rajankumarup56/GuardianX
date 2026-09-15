# GuardianX Agent Instructions

## 1. Product Identity

GuardianX is the internal codename for a defensive cybersecurity,
privacy, and safety layer for autonomous and connected cyber-physical
systems such as drones, robots, and other connected devices.

GuardianX is NOT a flight controller.

The primary flight/robot controller remains responsible for physical
control and native safety functions.

GuardianX provides an additional security, privacy, policy, monitoring,
risk, audit, and controlled-response layer.

---

## 2. Current Development Scope

Current phase:

V1 — Software-first Foundation and Security Core.

The current implementation must run locally on Windows.

Primary stack:

- Python
- FastAPI
- Uvicorn
- SQLite
- Pydantic
- pytest

Future technologies may include:

- Isolation Forest / explainable anomaly detection
- Raspberry Pi Edge
- PX4
- MAVLink
- ROS 2
- Android
- Web Command Center
- Cloud services
- Fleet management

Do NOT implement future components prematurely.

---

## 3. Architectural Principle

The system follows this logical architecture:

Owner
  ↓
Android/Web Command Center
  ↓
GuardianX Core Platform
  ↓
Identity / Authentication / RBAC
  ↓
Policy Engine
  ↓
Telemetry Ingestion
  ↓
Behaviour / Anomaly Analysis
  ↓
Risk Engine
  ↓
Privacy / Media Integrity
  ↓
Incident / Audit
  ↓
Safe Response Orchestrator
  ↓
GuardianX Edge
  ↓
PX4 / Robot Controller

During V1, physical hardware is simulated.

---

## 4. Security Principles

Always follow:

- Least privilege
- Defense in depth
- Zero-trust boundaries
- Explicit authentication
- Explicit authorization
- RBAC
- Secure password hashing
- Expiring sessions
- Input validation
- Auditability
- Secure defaults
- Data minimization
- Fail-safe behaviour
- No implicit trust based on network location

Never introduce:

- Hard-coded passwords
- API keys in source code
- Tokens in source code
- Secrets in documentation
- Disabled authentication for convenience
- Unsafe remote-control mechanisms
- Offensive security functionality
- Malware
- Persistence mechanisms
- Unauthorized command injection
- Weaponization features

---

## 5. AI/ML Rules

AI/ML is advisory.

AI/ML may:

- Detect behavioural anomalies
- Prioritize suspicious events
- Produce an anomaly score
- Provide supporting evidence

AI/ML must NOT independently override explicit safety
or security policy.

Deterministic security and safety policies remain authoritative.

All AI decisions should be explainable enough to show why
an event was considered suspicious.

---

## 6. Risk Decisions

The security decision vocabulary is:

- ALLOW
- ALERT
- RESTRICT
- BLOCK
- SAFE_RESPONSE

The exact decision must be determined by policy and risk logic.

Do not create arbitrary decision names without updating
the architecture and documentation.

---

## 7. Drone and Robot Safety

GuardianX must not replace native flight-controller failsafes.

For future PX4 integration:

- PX4 remains responsible for core flight safety.
- GuardianX provides security/policy decisions.
- GuardianX must not invent unsafe flight behaviour.
- Network loss must not automatically imply uncontrolled flight.
- Native PX4 failsafes remain authoritative.

Future integrations must consider:

- MAVLink authentication/signing
- Network segmentation
- Data-link loss
- Offboard loss
- Safe-state behaviour

---

## 8. Privacy

The system should support:

- Privacy zones
- Access control for media
- Audit logging of sensitive access
- Media integrity metadata
- Retention policies
- Data minimization

Do not collect unnecessary personal data.

Do not claim universal legal compliance.

Jurisdiction-specific legal requirements must remain configurable
and updatable.

---

## 9. Coding Rules

Prefer:

- Small modules
- Clear names
- Type hints
- Pydantic models
- Dependency injection where appropriate
- Testable services
- Explicit error handling
- Secure defaults

Avoid:

- Giant files
- Giant functions
- Hidden global state
- Duplicate business logic
- Premature abstractions
- Unnecessary dependencies

Every meaningful security decision should be testable.

---

## 10. Testing

Every new security-sensitive service must have tests.

At minimum test:

- Valid input
- Invalid input
- Boundary conditions
- Unauthorized behaviour
- Expected security decisions

Never remove existing tests merely to make a change pass.

---

## 11. Git Rules

Do not:

- Automatically commit
- Automatically push
- Force push
- Rewrite history
- Delete repositories
- Delete user files

unless explicitly instructed.

Before destructive changes, explain what will be changed.

Preferred workflow:

1. Implement
2. Run tests
3. Run application
4. User manually verifies
5. User approves commit
6. Commit
7. Push

---

## 12. Current Foundation Boundary

DO NOT implement yet:

- Real drone control
- Real PX4 commands
- Real MAVLink control
- Weapon systems
- Offensive cyber actions
- Payment processing
- E-commerce
- Production cloud infrastructure
- Play Store release
- Android production application
- Fleet billing
- Government procurement functionality

These belong to later phases.

---

## 13. Implementation Priority

Priority order:

1. Project foundation
2. Configuration
3. Database
4. Domain models
5. Health API
6. Identity/authentication
7. RBAC
8. Policy engine
9. Telemetry ingestion
10. Risk engine
11. Audit/event system
12. Simulation
13. Explainable anomaly detection
14. Web dashboard
15. Edge integration
16. PX4 integration
17. Android
18. Cloud/fleet
19. Commercialization

Do not skip foundational security controls to build UI faster.

---

## 14. Definition of Done

A feature is not complete merely because the code exists.

A feature is complete when:

- Code is implemented
- Tests pass
- Security assumptions are documented
- Error handling exists
- No secrets are committed
- Existing functionality still works
- Documentation is updated where required
- User can manually test the behaviour