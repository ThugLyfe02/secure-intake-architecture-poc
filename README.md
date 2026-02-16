# secure-intake-architecture-poc
Compliance-aware FastAPI backend architecture demonstrating regulated healthcare system design, security, and infrastructure maturity.
# Secure Intake Architecture POC

## Overview

This repository demonstrates a compliance-aware backend architecture for a regulated healthcare intake system. The goal is to showcase architectural maturity, security-first design, infrastructure awareness, and operational discipline appropriate for HIPAA-aligned environments.

This is not a feature demo. It is a system design exercise emphasizing risk reduction, auditability, and evolvability.

---

## Design Principles

- Security-first architecture
- Least privilege access control
- Field-level encryption for sensitive data
- Immutable audit logging
- Twelve-factor application compliance
- Infrastructure-as-Code ready
- Container orchestration neutrality (ECS ↔ EKS)

---

## High-Level Architecture

Client  
↓  
AWS Application Load Balancer (HTTPS)  
↓  
Containerized FastAPI Service (Stateless)  
↓  
PostgreSQL (RDS, encrypted at rest)  
↓  
S3 (Encrypted document storage via SSE-KMS)  
↓  
Centralized logging (CloudWatch / Structured JSON logs)

---

## Core Architectural Decisions

### Monolith Over Microservices

Chosen to reduce operational complexity, failure modes, and compliance surface area. System boundaries are internally modularized to allow future extraction if scale or organizational structure demands it.

### ECS Over EKS (Initial Bias)

ECS reduces operational overhead, cluster lifecycle management complexity, and misconfiguration risk. The system is designed container-first and orchestration-agnostic, allowing future migration to EKS if organizational scale justifies it.

### PostgreSQL Over NoSQL

The domain is relational, audit-heavy, and requires transactional integrity. ACID guarantees and strong indexing capabilities are prioritized over horizontal partition complexity.

---

## Security Model

### Authentication
- JWT-based authentication
- Short-lived access tokens
- Role-based access enforcement at API layer

### Authorization (RBAC)
Roles:
- Admin
- CaseWorker
- Reviewer

Authorization enforced server-side. No role trust from client.

### Encryption

- TLS enforced in transit
- RDS encryption at rest
- Field-level encryption for SSN and other PII
- KMS-managed keys

### Audit Logging

- Append-only audit log table
- All state mutations logged
- No PII stored in logs
- Structured JSON logging format

---

## Threat Model Considerations

- Insider misuse mitigation via RBAC + audit logs
- S3 public exposure prevention (block public access)
- IAM least privilege enforcement
- Secrets managed via AWS Secrets Manager
- Database private subnet isolation
- Infrastructure misconfiguration risk minimized via Terraform

---

## Observability & Reliability

- Stateless containers
- Horizontal scaling via load balancer
- Centralized structured logs
- Health check endpoints
- Backup and restore strategy defined
- Rollback strategy via immutable container versions

---

## Migration Strategy (ECS → EKS)

The application follows twelve-factor principles and remains fully containerized and stateless. Infrastructure modules are isolated in Terraform so orchestration layer changes are confined to infrastructure code rather than application logic.

Migration risk is minimized by:
- Avoiding orchestrator-specific dependencies
- Externalizing all state
- Using environment-based configuration

---

## Biggest Architectural Risks (Acknowledged)

- Poor data modeling
- Weak domain boundary enforcement
- IAM misconfiguration
- Logging sensitive information
- Lack of runbooks for incident response

Tooling choice is secondary to risk control.

---

## Purpose of This POC

To demonstrate how backend systems in regulated healthcare environments should be designed with:

- Controlled complexity
- Clear security boundaries
- Infrastructure foresight
- Evolvability
- Operational discipline

---

## Implementation Artifact

The file `secure_intake_demo.py` provides a minimal FastAPI implementation illustrating:

- Stateless API design
- JWT-based authentication structure
- Role-Based Access Control (RBAC)
- Field-level encryption abstraction for PII
- Audit logging middleware
- Twelve-factor configuration principles

This implementation is intentionally minimal to emphasize architectural clarity and security posture rather than feature breadth.

---

## Infrastructure Overview

The `infrastructure/` directory contains a minimal Terraform configuration demonstrating:

- Provider version pinning
- AWS region abstraction
- ECS cluster provisioning
- Fargate task definition
- IAM execution role configuration

This configuration is intentionally minimal to emphasize architectural clarity and deployment awareness rather than production-scale complexity.
