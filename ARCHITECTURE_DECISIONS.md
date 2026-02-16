# Architecture Decision Records (ADR)

This document captures key architectural tradeoffs made in this POC.
The goal is to demonstrate deliberate engineering decisions rather than accidental defaults.

---

## ADR-001: Monolith Over Microservices

**Decision:** Use a modular monolith.

**Rationale:**  
Given assumed team size and domain scope, microservices would increase operational complexity, failure modes, and compliance surface area unnecessarily.  
Internal modularization allows future service extraction if scale demands it.

---

## ADR-002: ECS Over EKS (Initial Bias)

**Decision:** Favor ECS for initial deployment.

**Rationale:**  
ECS reduces cluster lifecycle overhead and Kubernetes-specific operational risk.  
Design remains orchestration-neutral to allow migration to EKS if organizational scale or platform maturity justifies it.

---

## ADR-003: PostgreSQL Over NoSQL

**Decision:** Use PostgreSQL as primary datastore.

**Rationale:**  
The domain requires relational integrity, transactional consistency, and audit traceability.  
ACID guarantees are prioritized over horizontal partitioning complexity.

---

## ADR-004: Field-Level Encryption

**Decision:** Encrypt sensitive fields prior to persistence.

**Rationale:**  
Database-level encryption protects at-rest storage but does not fully mitigate insider misuse or query exposure risk.  
Field-level encryption reduces blast radius.

---

## ADR-005: RBAC Over ABAC

**Decision:** Use role-based access control.

**Rationale:**  
RBAC provides clarity, predictability, and audit simplicity in regulated environments.  
Attribute-based policies introduce complexity and testing overhead.

---

## ADR-006: Stateless Application Design

**Decision:** Design API as fully stateless.

**Rationale:**  
Stateless services simplify horizontal scaling, reduce migration risk between orchestration layers, and improve failure recovery patterns.

---

## Meta-Principle

Tooling choices are secondary to risk control, data integrity, and security boundaries.
