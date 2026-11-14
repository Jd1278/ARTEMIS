# Operational constraints and technical verification

Report 010. English submission edition. Date: 14 November 2026. Version 1.0. Sequential investigation 6 of 7. Documentary and local verification complete. No remote database or space-environment validation.

## Question and conclusion

What should happen when communication, data or components fail? Distinguish interface availability, API, storage and external link. The architecture depends on Supabase for persistence and does not establish autonomous space operation. It can be investigated as a connected prototype with possible later local storage and synchronization.

After report 009 closed, commit `80be128b17b5046ecd267d5a0604bbc5c74f5444` was fixed. It adds visual identity relative to report 004 but retains the API scaffold. Requirements and connection code were inspected and tests ran in an isolated checkout. Only the research evidence file was written outside that checkout. No remote database was accessed.

[NASA/TM-2019-220335](https://ntrs.nasa.gov/citations/20200001702) describes exploration medical communication and evacuation/resupply constraints. These motivate continuity and autonomy, but slow terrestrial networking does not reproduce the full space context. [Supabase connection documentation](https://supabase.com/docs/guides/database/connecting-to-postgres) describes pool/connection considerations, not elimination of remote dependence.

## Executed checks

[Evidence JSON](../evidence/010_operacion.json) preserves commands, output and in-process HTTP responses under Python 3.13.1.

| Check | Result | Meaning |
| --- | --- | --- |
| Contract/artifact unit tests | Two passed, exit 0 | Data coverage, not full product workflow |
| Package validator | 46 PASS, exit 0 | Consistency with rules, not clinical validity |
| P0 artifact | 4,320 synthetic observations, six profiles, 92 nulls | Prepared demonstration selection |
| GET `/api/health` | 200, scaffold, database unchecked | Service entry only |
| GET profiles, indicators, example dashboard | 404 | Product routes absent |
| POST observations, fictional example | 404 | No save or Supabase contact |

The 404 results describe unfinished functionality, not accepted workflows. FastAPI TestClient operated inside the process. There was no public server or space network. The frontend remains reserved with logo and visual tokens, not a functional interaction.

## Failure matrix for later evaluation

| Condition | Proposed behavior | Required evidence | Status |
| --- | --- | --- | --- |
| API unavailable | Clear message and draft under agreed scope | Interrupt API during task | Pending integration |
| Supabase unreachable | No false save confirmation; session draft | Timeout test | Pending |
| Response lost after save | Idempotent retry | One stored row; conflict for altered UUID content | Designed, not remotely verified |
| Old/missing data | Visible age or absence | Fixed cases and table/chart agreement | Pending UI |
| Invalid or incompatible input | Explain rejection without partial write | API/SQL tests in test environment | Constraints written, integration pending |
| Profile/origin changed | Separate histories and references | Multiple-profile/source cases | Contract prepared |
| Close/restart | Explicit durable and nondurable state | Controlled client/server restart | Pending |

## Levels of autonomy

A connected demonstration stores remotely when a link exists and is the present intended scope, still awaiting integration. Durable local operation additionally needs appropriate local storage, bundled resources and recovery tests. Operation across disrupted links adds queues, synchronization, conflict management, audit and operational procedures. That third level is future research.

Finish and measure the selected level before adding unnecessary distributed services. Before claiming offline support, test reload, closure, restart, retries and persistence without an external link.

## Decisions and limits

Separate sent from confirmed saved. Preserve source, quality and time. Version comparisons and expose fictional calendar context. SQL and RLS definitions need authorized remote verification and do not replace API controls.

Performance, energy, radiation tolerance, sensor accuracy, usability and full security were not measured. No dependencies, migrations or publications were performed. These checks do not establish flight readiness.

## Closure and sources

The fixed-snapshot operational investigation is complete. A full save–retrieve–restart workflow and connection failure test are the next useful evidence. Marketing should describe development and intended follow-up rather than proven offline autonomy or implemented real-time monitoring.

Technical sources: [requirements](https://github.com/Jd1278/ARTEMIS/blob/80be128b17b5046ecd267d5a0604bbc5c74f5444/artemis-healt/docs/requirements.md), [API](https://github.com/Jd1278/ARTEMIS/blob/80be128b17b5046ecd267d5a0604bbc5c74f5444/artemis-healt/src/artemis_health/main.py), [Supabase design](https://github.com/Jd1278/ARTEMIS/blob/80be128b17b5046ecd267d5a0604bbc5c74f5444/artemis-healt/docs/supabase.md).
