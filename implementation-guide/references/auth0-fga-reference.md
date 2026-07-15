# Auth0 Fine-Grained Authorization (FGA) Reference

## Platform Components

Use these component names consistently across all documents. Map use cases to the appropriate components.

### Core Fine-Grained Authorization Components

| Component | What It Does | Common Use Cases |
|-----------|-------------|------------------|
| **Auth0 FGA** | Managed relationship-based access control (ReBAC) service, built on OpenFGA | All fine-grained/application-level authorization use cases |
| **Authorization Model** | Type definitions (declared in the FGA modeling language/DSL, `.fga` files) that describe which relations are possible between users and objects | Defining the permission structure of an app (owner, editor, viewer, member, etc.) |
| **Stores** | Isolated containers for one authorization model (with version history) plus its relationship tuples | Separating environments (dev/staging/prod) or separating tenants/products |
| **Relationship Tuples** | The base fact records — a `user`, `relation`, and `object` triplet (optionally with a condition) — that get written to a store | Granting a specific user or group a specific relationship to a specific resource |
| **Check API** | Real-time API call that answers "does this user have this relation to this object?" (`{"allowed": true/false}`) | Authorization check in the request path (can this user open this document?) |
| **ListObjects API** | Returns all objects of a given type that a user has a specified relationship with | Populating a filtered list view ("show me all documents I can edit") |
| **ListUsers API** | Returns all users (or groups) that have a specified relationship with a given object | "Who has access to this folder?" audit/sharing-panel views |
| **Contextual Tuples** | Tuples supplied at request time (Check/ListObjects/ListUsers/Expand only) without being persisted to the store | Injecting session/token attributes (e.g., current IP, device trust) into a check without writing them to the datastore |
| **Conditions** | CEL-expression-based rules attached to a relationship tuple that must evaluate true for the tuple to apply | ABAC-style rules layered on ReBAC (e.g., only valid during business hours, only if resource.status = active) |

### Supporting Components

| Component | What It Does |
|-----------|-------------|
| **OpenFGA** | The open-source engine Auth0 FGA is built on; a CNCF project (Incubating, as of October 2025) | 
| **FGA Modeling Language (DSL)** | Human-friendly syntax for authorization models; compiles to the JSON syntax the API actually consumes |
| **FGA Playground** | Hosted sandbox (play.fga.dev) for building and testing a model and tuples interactively |
| **SDKs** | Official client libraries for Node.js/JavaScript, Python, Go, Java, and .NET (published under the `openfga` GitHub org; older `auth0-lab` SDKs are deprecated) |
| **CLI / IDE Extensions** | `fga` CLI plus VS Code and IntelliJ extensions for authoring and validating `.fga` model files |
| **Assertions** | Test cases attached to a model version that assert expected Check results, used to validate a model before deploying it |

### Important Distinctions

**ReBAC vs RBAC vs ABAC**
- **RBAC** (role-based): access is granted by assigning a user to a coarse role (admin, editor). Simple, but roles multiply as an app needs per-resource nuance.
- **ABAC** (attribute-based): access is computed from attributes/rules at evaluation time (department = Finance AND resource.classification = public).
- **ReBAC** (relationship-based, what FGA does): access is derived from a graph of relationships between users and objects (this user is an editor of this document; this document's parent folder is owned by this team). FGA layers Conditions on top of ReBAC tuples to pull in ABAC-style logic where needed — it is not a pure ReBAC-only tool in practice.

**Auth0 FGA authorization vs Auth0 CIC authentication**
- Auth0 FGA answers "what can this already-identified user do?" — it is an authorization decision engine, not an identity provider.
- Auth0 Customer Identity Cloud (CIC) — see the companion `auth0-cic-reference.md` — handles authentication, MFA, user registration, and login/session management, plus basic RBAC (roles/permissions on the token).
- These are frequently paired: CIC authenticates the user and issues a token; the application then calls FGA's Check API (often passing token claims in as contextual tuples) to make the fine-grained access decision. Do not conflate CIC's built-in RBAC roles/permissions feature with FGA — FGA is for authorization models that outgrow flat roles (per-resource, per-relationship, hierarchical, multi-tenant).

**Managed Auth0 FGA vs self-hosted OpenFGA**
- **Auth0 FGA** is the managed, hosted SaaS offering — Auth0/Okta operates the store, model versioning, playground, and API endpoints.
- **OpenFGA** is the underlying open-source engine (CNCF Incubating project); it can be self-hosted on the customer's own infrastructure with the same API surface and modeling language.
- The choice matters for discovery: self-hosting shifts operational burden (uptime, scaling, upgrades) to the customer but removes any data-residency/vendor dependency concerns; the managed service removes operational burden but is a paid product with its own SLAs and jurisdiction/data-residency options.

---

## Common Fine-Grained Authorization Use Case Patterns

### Document/Folder Sharing Permissions (Google-Drive-style)

**Typical flow:**
User creates or is granted access to a document → tuple written (user, relation, document) → another user attempts to open the document → app calls Check API → FGA resolves tuple graph (direct share, or inherited via folder) → allow/deny returned → app renders or blocks content

**Key components:** Authorization Model (owner/editor/viewer relations), Relationship Tuples, Check API, ListUsers API (for "who has access" panels), ListObjects API (for "my documents" views)

**Discovery questions:**
- What relations exist beyond owner/editor/viewer (commenter, downloader, share-manager)?
- Can access be inherited from a parent folder, or is every document shared individually?
- Do public/anyone-with-link shares need to be modeled (the `*` wildcard user)?
- How is a share revoked — deleting a tuple, or expiring a condition?
- What is the expected latency budget for the sharing-panel "who has access" query on large documents?

### Hierarchical/Nested Resource Permissions

**Typical flow:**
Resource created under a parent (folder under folder, project under workspace) → tuple links child to parent → user requests access to child → Check API evaluates direct tuples first, then walks the tuple-to-userset chain up the hierarchy → allow/deny returned

**Key components:** Authorization Model (parent-child type relations, tuple-to-userset syntax), Relationship Tuples, Check API, Conditions (for hierarchy exceptions)

**Discovery questions:**
- How deep does the hierarchy go, and is depth fixed or arbitrary (folders-within-folders)?
- Should permissions always inherit downward, or can a child override/restrict what a parent grants?
- Are there resources that need to break inheritance entirely (a locked-down sub-folder)?
- How are moves handled — does moving a resource to a new parent automatically change effective access?
- What is the tuple-write volume when a large hierarchy's permissions change in bulk (e.g., reorganizing a workspace)?

### Multi-Tenant Application Authorization

**Typical flow:**
User authenticates and is scoped to a tenant/organization (via CIC or another IdP) → app calls Check API with tenant/org as part of the object or as a contextual tuple → FGA confirms user's relationship within that tenant's boundary → access decision returned

**Key components:** Authorization Model (organization/tenant type as a first-class object), Relationship Tuples, Contextual Tuples (for token-derived tenant context), Stores (single store with tenant-scoped types is typical; a store-per-tenant is possible but less common at scale)

**Discovery questions:**
- Is tenant isolation modeled within one store (tenant as a type) or via separate stores per tenant?
- Can a single user belong to multiple tenants, and if so, how is the active tenant selected at request time?
- Do cross-tenant relationships ever need to exist (a vendor with access into multiple customer tenants)?
- How are tenant-level admin roles distinguished from resource-level relations within that tenant?
- What is the expected tuple volume per tenant, and does that change the store/model design?

### RBAC-at-Scale (Beyond Simple Roles)

**Typical flow:**
App currently assigns coarse roles (admin/member) → team hits a wall where roles need per-resource or per-team nuance → relations are modeled per resource type instead of a single global role → existing role assignments migrated into tuples → Check API replaces in-app role checks

**Key components:** Authorization Model (replacing a flat roles table with typed relations), Relationship Tuples (bulk-migrated from existing role/user tables), Check API, ListObjects API (replacing "get all resources this role can see" queries)

**Discovery questions:**
- What specific scenario is the current RBAC system failing at (per-resource exceptions, per-team roles, temporary elevated access)?
- Where does the source-of-truth for existing roles live today, and what is the migration path to tuples?
- Will the app fully replace in-code role checks with Check API calls, or run both in parallel during transition?
- Are there performance-sensitive code paths (page load, list rendering) that will now depend on FGA response times?
- Who owns the authorization model going forward — is model-authoring a developer task, or does it need an admin UI on top?

### Relationship-Based Access Checks in an App Request Path

**Typical flow:**
Incoming API request → app authenticates the caller (via CIC/OIDC) → app extracts the resource ID from the request → app calls FGA Check (optionally with contextual tuples from the token) → FGA returns allow/deny → app proceeds or returns 403 → decision optionally logged for audit

**Key components:** Check API, Contextual Tuples (token claims passed in without persisting), Conditions (for time/attribute-bound rules), Relationship Tuples

**Discovery questions:**
- Where in the request pipeline does the Check call happen (middleware, per-endpoint, gateway-level)?
- What is the acceptable added latency per request, and has caching or batching been considered?
- Does the check need to happen before every read/write, or only for specific sensitive operations?
- How are Check failures (network error, timeout) handled — fail-open or fail-closed?
- Is there a need to batch multiple checks per request (e.g., checking access to 50 rows in a list), and has the app been designed to use ListObjects/ListUsers instead of N individual Check calls where possible?

---

## Honest Capability Assessment

When creating implementation guides, be accurate about what Auth0 FGA can and cannot do natively. Do not overstate capabilities.

### Strengths (lean into these)
- Purpose-built for relationship graphs that flat RBAC roles cannot express cleanly (nested resources, per-object sharing, multi-tenant scoping)
- Backed by the Zanzibar-style architecture and OpenFGA's proven scale characteristics (billions of tuples, high request throughput)
- Conditions add ABAC-style flexibility on top of ReBAC without needing a separate policy engine
- Contextual Tuples let an app supply request-time context (token claims, session attributes) without writing extra data to the store
- Managed service removes the operational burden of running OpenFGA yourself, while staying compatible with the open-source engine and its modeling language
- ListObjects/ListUsers give search-shaped answers (all objects a user can see, all users who can see an object) instead of forcing N individual Check calls

### Gaps to Acknowledge (document as discovery items, not limitations)
- **Application integration effort**: FGA does not sit in the request path automatically — the application must be changed to call Check/ListObjects/ListUsers at the right points, and to keep tuples in sync as data changes. This is real engineering work, not a drop-in config.
- **Model design complexity**: designing a correct authorization model (types, relations, tuple-to-userset chains) is a non-trivial exercise, closer to schema design than form configuration. Poorly designed models can be hard to refactor once tuples exist in production.
- **Tuple/data synchronization**: relationship tuples are a separate data store from the application's own database. Keeping tuples consistent with the source of truth (e.g., when a document is deleted or reassigned) is the application's responsibility — FGA does not watch the app's database for changes.
- **Latency and caching considerations**: every fine-grained check is a network call. High-traffic, low-latency paths (e.g., rendering a list of 200 rows) need batching (ListObjects) or caching strategy; naive per-row Check calls will not scale well without one.
- **No native admin/reviewer UI for business users**: model authoring is done via the DSL/CLI/Playground, aimed at developers. There is no built-in end-user-facing "who can see what" governance console comparable to Okta OIG's certification campaigns — building that view is left to the application team.
- **Maturity relative to OIG-style governance**: FGA is an authorization decision engine, not a governance/certification platform. It does not include access-review campaigns, approval workflows, or SoD policy enforcement out of the box — those would need to be built on top, or paired with a separate governance layer.

Frame gaps as discovery items: "Validate whether the application's request path can absorb the added Check/ListObjects call, and whether the team has capacity to design and maintain the authorization model, or if this needs a dedicated modeling engagement."

---

## Diagram Component Mapping

When creating Mermaid diagrams for Auth0 FGA, use these class assignments:

| FGA Component | Mermaid Class |
|---------------|---------------|
| End user action, incoming API request | `trigger` |
| CIC/IdP, application's own database, external caller | `extSystem` |
| Auth0 FGA / OpenFGA engine, Store | `platform` |
| Model authoring, tuple sync automation (if scripted) | `workflow` |
| Check API result, policy/condition evaluation | `decision` |
| Authorization Model, Conditions, relationship graph evaluation | `governance` |
| Writing/updating Relationship Tuples, ListObjects/ListUsers calls | `action` |
| Access granted, request fulfilled | `endpoint` |
| Access denied (403), Check returns false | `danger` |
| Audit log of tuple changes or access decisions | `audit` |
| Alert on unexpected denial patterns, ops notification | `notify` |
