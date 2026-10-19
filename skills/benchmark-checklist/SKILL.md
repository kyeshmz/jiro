---
name: benchmark-checklist
description: Vet a performance claim against its limiter, production tuning, physical limits, errors, repeatability, relevance, and proof that timed work happened. Use for @benchmark-checklist, a benchmark, or a measured speedup or regression before reporting or choosing an option.
license: MIT
metadata:
  opencode/autoinvoke: false
---

# Benchmark checklist

Answer with run evidence, not a guess from reading code. Read `references/shared-rules.md` first. Resolve bundled resources from the loaded skill base and run measurements in the target project. Use its existing harness before adding tooling. Do not stop unrelated jobs or change production resources to make a cleaner measurement.

For an explicitly requested quick ballpark, one run can suffice. Still check errors and that timed work happened. Say it was one run and skip the remaining checks only when it looks plausible. A decision between options is not a ballpark.

## Before measuring

1. Write the exact claim you expect to report, including metric, unit, percentile when relevant, workload, and data size.
2. Read the measurement script. Identify what it times, counts, and excludes.
3. Check machine load with `uptime` and core count with `nproc`, or the platform equivalent. Investigate competing load. If it cannot be removed within scope, interleave both sides under the same noise and disclose it.

## Seven checks

1. **Name the limiter.** Ask why performance cannot double. Profile a separate run that is not included in the reported timing. Inspect per-process CPU, runtime profiles, I/O wait, syscall counts, and the load generator as appropriate. Map the hot spot to source. A saturated load generator measures itself. If a change moves nothing, find the limiter before declaring the change useless.
2. **Tune every side fairly.** Match production builds, flags, environment, batching, transactions, pools, cache state, versions, and data. Defaults versus tuned settings compare configurations, not implementations. A debug build, missing index, or commit per row is an untuned side. Tune and rerun before selecting an option. If tuning is blocked, do not pick a winner. Narrowing the wording to current settings does not settle what a user should adopt.
3. **Check physical and causal limits.** Compare throughput with disk and network bandwidth. Compare operations times CPU cost with available cores. Compare claimed savings with the fraction of time the changed component took. Removing a component that used 10% of runtime can cut duration by at most 10%, or increase throughput by about 11%. Exceeding a bound suggests cached work, a no-op, or a bug.
4. **Count errors and validate outputs.** Count failures, rejected requests, non-success responses, timeouts, and retries. Check actual correctness, not just output presence. Fast failures and slow retries distort results. Add missing error counts to an authorized harness change, or mark the measurement incomplete.
5. **Repeat without favoring a side.** Run each side at least five times in alternating order. Account for warmup, lazy initialization, caches, and drift. Report the median and range. A gap smaller than run-to-run variation is no measurable difference. For a close result, use the harness's statistics or a suitable rank-sum test rather than guessing from one best run.
6. **Measure what users wait for.** Pair a microbenchmark with the end-to-end path at realistic sizes and concurrency. Report the micro path's share of total time. Making a helper that consumes 1% of a request infinitely fast can remove at most that 1% of duration.
7. **Prove the work happened inside the timer.** Confirm requests reached the server, rows were written, bytes were read, and results were consumed. Iterate lazy generators, await promises, and prevent discarded results. A timeout or deferred operation is not completion of the timed work.

## Use the result

Vet a performance baseline before planning from it. For repeated optimization, vet the harness before freezing the comparison method. Make that harness print error counts and completed-work counts so every iteration checks them. Use `show-me-your-work` for a long run and record only changes this task owns. Never reset unrelated edits while discarding an unsuccessful experiment.

## Report

Lead with faster, slower, no measurable difference, or inconclusive. Give the number and unit, workload, count per side, median and range, limiter, correctness evidence, and completed-work evidence. State environment noise and any tuning mismatch.

Call a claimed difference inconclusive if its limiter is unknown, a side is untuned, or errors and completed work could not be checked. Name the gap. Keep PR prose to one primary number when that is the requested deliverable. Put run details and limiter evidence in a real linked artifact or local notes, without creating or publishing a PR unless authorized.
