# Synapse by [Ax Lab](https://axiomaticlab.com/) 

**A modular semantic and governace framework for secure, scalable, and interoperable data ecosystems**

## **Overview**
Synapse is the missing link between chaotic data silos and enterprise-grade governance.

While most platforms focus on AI, analytics, or raw data storage, Synapse provides the Semantic & Governance Layer that ensures data integrity, compliance, and interoperability across systems. It is designed for regulated industries, federated data networks, and multi-party collaboration, where trust, traceability, and standardization are critical.

Synapse project is an Open Source project designed as a **modular, scalable, and secure** data management system with capabilities for **database connections, API integrations, local file processing, and custom function execution**. It leverages Django’s **ORM, forms, views, and middleware** to provide a robust backend while ensuring **data integrity, security, and performance**.

    "Synapse doesn’t just move data—it governs it."


### **Key Objectives**
1. **User Management & Authentication**
   - Role-based access control (staff, stakeholder, other).
   - Secure credential storage (encrypted passwords, API keys).

2. **Database & API Integration**
   - Support for **PostgreSQL, SQLite, and other database types**.
   - **API connection management** with OAuth2/JWT support.

3. **Data Processing & Automation**
   - **Local file ingestion** (Excel, CSV) with schema validation.
   - **Custom function execution** (Python scripts, mappings).

4. **Scalability & Performance**
   - **Modular design** for horizontal scaling.
   - **Caching strategies** for optimized query performance.

5. **Security & Compliance**
   - **Encrypted credentials** (database passwords, API keys).
   - **Role-based access control (RBAC)** for sensitive operations.

---

## **Technical Architecture**

### **1. Core Components**
| **Component**               | **Description**                                                                                     | **Technologies Used**                     |
|-----------------------------|----------------------------------|--------------------------------------------|
| **User Management**         | Handles user registration, authentication, and role-based permissions.                             | Django `User` model, `user_info` model.    |
| **Database Connections**    | Manages connections to external databases (PostgreSQL, SQLite, etc.).                              | `database_connection`, `database_user_connection`. |
| **API Connections**         | Stores and manages API credentials for third-party integrations.                                   | `api_connection`, encrypted fields.        |
| **Data Tables & Mappings**  | Links users to database tables or mappings with type enforcement (`data`, `mapping`, `other`).     | `datatable_connection`, `datatable_groups`. |
| **Local File Processing**   | Handles uploads and processing of Excel/CSV files.                                                 | `local_data_files`, `local_function_files`. |
| **Custom Functions**        | Executes user-defined functions (Python scripts, mappings, actions).                               | `connection_functions`, `input_value_to_connections_function`. |
| **Dictionary Keys**         | Acts as a lookup system for column mappings (e.g., `age` → `Demographics`).                        | `dictionary_keys`, `datatable_dictionary`. |

---

### **2. Unique Technical Specifications**
#### **A. Security & Encryption**
- **Encrypted Credentials**:
  - Database passwords (`_db_password`) and API keys (`_api_password`, `_api_key`) are **encrypted using Django’s `signing` utility**.
  - Example:
    ```python
    from django.core import signing
    encrypted_password = signing.dumps(db_password)  # Encrypt
    decrypted_password = signing.loads(encrypted_password)  # Decrypt
    ```
- **Authentication & Authorization**:
  - **Role-based access control (RBAC)** via `user_type` field in `user_info`.
  - **Custom middleware** (e.g., `SecurityHeadersMiddleware`) for security hardening.

#### **B. Database & ORM Optimizations**
- **Dynamic Table Connections**:
  - Users can link to **specific database tables** via `datatable_connection`, filtered by their permissions.
  - Example:
    ```python
    user_tables = datatable_connection.objects.filter(user=request.user)
    ```


#### **C. File Processing & Automation**
- **Local File Ingestion**:
  - Supports **Excel (`.xlsx`) and CSV (`.csv`)** files via `local_data_files`.
  - **Schema validation** ensures correct column mappings.
  - Example:
    ```python
    import pandas as pd
    df = pd.read_excel(local_data_files.local_file_path)
    ```
- **Custom Function Execution**:
  - Users can define **Python scripts** (`local_function_files`) or **mappings** (`function_type`).
  - Example:
    ```python
    from myapp.models import connection_functions
    function = connection_functions.objects.get(name="data_processing")
    ```

#### **D. API Integration**
  - Secure API connections via `api_connection` model.
  - Example:
    ```python
    api_conn = api_connection.objects.get(api_base_url="https://api.example.com")
    ```



---

## **Models & Data Schema**

### **1. `user_info`**
- **Purpose**: Stores user profiles with role-based access.
- **Key Fields**:
  - `user_type`: Choices (`'staff'`, `'stakeholder'`, `'other'`).
  - `user_email`: Unique email for authentication.
  - **Foreign Key**: Links to Django’s built-in `User` model.

### **2. `database_connection`**
- **Purpose**: Manages external database connections.
- **Key Fields**:
  - `database_type`: Choices (`'postgres'`, `'sqlite'`, `'other'`).
  - `database_url`: Connection string (e.g., `postgres://user:pass@localhost:5432/db`).
  - `database_port`: Default `5432` (PostgreSQL).

### **3. `api_connection`**
- **Purpose**: Stores API credentials securely.
- **Key Fields**:
  - `api_base_url`: Unique base URL for the API.
  - `_api_password` / `_api_key`: **Encrypted** credentials.

### **4. `datatable_connection`**
- **Purpose**: Links users to database tables.
- **Key Fields**:
  - `datatable_name`: Name of the table.
  - `databale_type`: Choices (`'data'`, `'mapping'`, `'other'`).

### **5. `local_data_files`**
- **Purpose**: Handles local file uploads.
- **Key Fields**:
  - `local_file_type`: Choices (`'xlsx'`, `'csv'`, `'other'`).
  - `local_file_path`: Path to the uploaded file.

### **6. `connection_functions`**
- **Purpose**: Executes custom functions (Python scripts, mappings).
- **Key Fields**:
  - `function_type`: Choices (`'data'`, `'mapping'`, `'action'`, `'other'`).
  - `function_input_values_schema`: JSON schema for inputs.

---

## **Forms & User Input Handling**

### **1. Form Structure**
- **All forms are `ModelForm` instances** tied to the models in `models.py`.
- **Key Forms**:
  - `create_datatable_connection`: Links users to database tables.
  - `create_api_connection`: Securely stores API credentials.
  - `local_file_to_db`: Processes local file uploads.

### **2. Dynamic Dropdowns**
- **Custom `ModelChoiceField` classes** (e.g., `input_conn_for_input_value_conn`) populate dropdowns based on user permissions.
- Example:
  ```python
  class create_datatable_connection_form(forms.ModelForm):
      user_db_connection = forms.ModelChoiceField(
          queryset=database_user_connection.objects.filter(user=request.user)
      )
  ```

### **3. Security in Forms**
- **Encrypted Field Handling**:
  - Passwords and API keys are **never stored plaintext** (e.g., `_db_password`).
  - Example:
    ```python
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance._db_password = signing.dumps(self.cleaned_data['db_password'])
        if commit:
            instance.save()
        return instance
    ```

---

## **Security Measures**

### **1. Authentication & Authorization**
- **Django’s Built-in Auth**:
  - Uses `django.contrib.auth` for user management.
- **Role-Based Access**:
  - `user_type` field restricts access to certain features.

### **2. Data Encryption**
- **Credential Encryption**:
  - Uses Django’s `signing` utility for passwords and API keys.
  - Example:
    ```python
    from django.core import signing
    encrypted = signing.dumps("my_secret_password")
    decrypted = signing.loads(encrypted)
    ```

### **3. Input Validation**
- **Form Validation**:
  - Ensures correct data types (e.g., `database_type` choices).
- **Sanitization**:
  - Prevents SQL injection via Django ORM.


---

## **Additional Resources**

### **1. Useful Links**
- [Django Documentation](https://docs.djangoproject.com/)


### **2. Glossary**
| **Term**               | **Definition**                                                                                     |
|------------------------|---------------------------------------------------------------------------------------------------|
| **ORM**                | Object-Relational Mapping (Django’s database abstraction layer).                                |
| **RBAC**               | Role-Based Access Control (restricts system access based on user roles).                         |
| **IaC**                | Infrastructure as Code (e.g., Terraform, Ansible).                                                |

---

## **📝 Conclusion**
This Django project is designed for **scalability, security, and modularity**, with strong support for **database connections, API integrations, and local file processing**. Key strengths include:
✅ **Role-based access control** for security.
✅ **Encrypted credential storage** for sensitive data.
✅ **Dynamic form handling** for user input.
✅ **Containerization & cloud deployment** for scalability.
✅ **Monitoring & observability** for reliability.



---

## [Ax Lab](https://axiomaticlab.com): Doing what is Obvious
Redefining Automation Through Task-Based Intelligence & Radical Control.

-----------------

### Our Mission
Modern AI is often a "black box"—unpredictable, over-privileged, and brittle. Ax Lab exists to bring common sense back to automation. 
We don’t just deploy scripts; we **onboard intelligence.** Our systems are designed to perform individual tasks with the same logic, security clearance, and auditability as your best human hire.

------------------------------
## The Architectural Moat: Our Four-Layer Stack

Axiom, our main product, is the Governance, Semancti, & Action Layer for Digital Labor
Most agentic workflows fail because they are purely probabilistic. Ax Lab wins by unifying the four critical layers of enterprise-grade digital labor:

* **The Reasoning Layer (Daemon)**: A secure "background brain" that manages the logic split between local privacy and API power while maintaining organizational memory.
* **The Governance Layer (Synapse)**: Our "Access Control" moat. Synapse ensures that AI agents operate with granular User-Security Level Attribution, preventing "Shadow AI" and unauthorized data access.
* **The Action Layer (Cadence)**: A rhythmic, repeatable orchestrator. Cadence manages task dependency logic, allowing for Surgical Correction—if a 20-step process fails at step 12, you fix the task, not the workflow.
* **The Semantic Layer(Synapse)**: The interface between unstructured data and structured execution, ensuring the AI understands your business logic as intuitively as a human hire.

## Key Product Features

**1. Deterministic Task Onboarding**
We don't "prompt" agents; we onboard workers. Ax Lab converts intuitive business processes into autonomous, task-level building blocks. If a process is documented, it is automatable with 100% auditability.

**2. Hierarchical Permissioning (Fail-to-Human)**
AI shouldn't have "God Mode."

* Attribute-Based Access Control (ABAC): Every automated action is signed with a security clearance level, mirroring your existing corporate hierarchy.
* The Trust Gap Bridge: We solve the liability shift. When an agent encounters an edge case, it triggers a "Fail-to-Human" handoff, ensuring 0% hallucination in critical paths.

**3. Non-Linear Process Resilience**
Standard automation is brittle. Ax Lab is Dynamic.

* Modular Recovery: Audit, modify, and resume individual tasks mid-stream without disrupting the entire orchestration.
* Operational Momentum: Eliminate the "Restart from Step 1" cost, saving thousands in compute and manual overhead.

**4 Approach:**

**- 1. The "Obvious" Workflow**
We focus on intuitive, task-level building blocks. If a process is clear enough for a human to follow, it’s a candidate for Ax Lab automation. We turn the obvious into the autonomous.

**- 2. Hierarchical Security (User-Level Attribution)**
AI shouldn't have a "God Mode" key to your database.

* Granular Permissions: Every single task in our orchestration is assigned a specific user-security level.
* Strict Access: Our AI respects your existing organizational hierarchy, interacting only with the data it is cleared to see.

**- 3. Non-Linear Resilience (Surgical Correction)**
Stop wasting time on "restart from Step 1."

* Modular Recovery: If a 20-step process fails at step 12, you can audit, fix, and resume at step 12.
* Dynamic Orchestration: Correct individual tasks mid-process without disrupting the entire workflow, saving compute time and operational momentum.

------------------------------
## Our Approach: Onboarding vs. Integration
We believe the best AI behaves like a professional. Our "Onboarding" framework ensures:

* Auditability: Real-time logging of who (which agent) did what, and under what authority.
* Agility: Swap, upgrade, or pause individual tasks without breaking the system.
* Transparency: No black boxes. Just logic you can see, verify, and trust.

------------------------------
## 🤝 Work With Us
We are looking for partners and enterprises ready to move past the AI hype and into high-utility, high-security operations.

* For Enterprises: Secure your automation and eliminate process fragility.
* For Visionaries: Help us define the next era of "Obvious" intelligence.

[Explore Our Youtube Channel](https://www.youtube.com/channel/UCltGi4Su305oln_ldu-b94Q) | [Inquire About a Pilot](https://axiomaticlab.com) | [View Our LinkedIn](https://www.linkedin.com/company/axiomatic-lab/)