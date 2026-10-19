# TypeScript patterns

Read this file from the loaded skill's base directory. These examples support `typescript-best-practices`. `principle-type-system-discipline` owns the language-independent type rules. `principle-boundary-discipline` owns validation placement.

## Contents

- [Branded types](#branded-types).
- [Discriminated unions](#discriminated-unions).
- [Constructive modeling](#constructive-modeling).
- [Simplest total type](#simplest-total-type).
- [Unknown external input](#unknown-external-input).
- [Schemas before hand-written guards](#schemas-before-hand-written-guards).
- [Avoid unchecked assertions](#avoid-unchecked-assertions).
- [Narrowing order](#narrowing-order).
- [Sound type guards](#sound-type-guards).
- [Exhaustiveness](#exhaustiveness).
- [Satisfies and literal types](#satisfies-and-literal-types).
- [Boundary validation](#boundary-validation).
- [Derived types](#derived-types).
- [Object arguments](#object-arguments).
- [Real tests and diagnostics](#real-tests-and-diagnostics).

## Branded types

Use different types for different semantic values. Validate once at creation. Internal callers can then trust the result.

```ts
type AgentId = string & { readonly __brand: "AgentId" };

function isAgentId(input: string): input is AgentId {
	return /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(input);
}

function parseAgentId(input: unknown): AgentId {
	if (typeof input !== "string" || !isAgentId(input)) {
		throw new Error("Invalid agent ID");
	}
	return input;
}

function focusAgent(id: AgentId): AgentId {
	return id;
}
```

The example checks a UUID-shaped string. Use the repository's actual ID specification and validator for real input. A well-formed ID does not prove that an agent exists or that access is authorized.

Follow the repository's existing branding convention. Do not introduce an incompatible second convention. Without an existing convention, use the `readonly __brand` shape above. A bare `as AgentId` proves nothing.

## Discriminated unions

A boolean plus optional fields permits contradictory states.

```ts
type LooseDiffState = {
	loading: boolean;
	diff?: GitDiff;
	error?: string;
};
```

A literal discriminant ties each state to the data it owns.

```ts
type DiffState =
	| { kind: "loading" }
	| { kind: "ready"; diff: GitDiff }
	| { kind: "error"; error: string };
```

Use one discriminant name consistently within a domain. Follow an established `kind`, `type`, or `tag` convention.

## Constructive modeling

Build a legal value from legal parts instead of passing a loose value with a comment about its invariant.

```ts
type NonEmpty<T> = [T, ...T[]];

function firstEntry<T>(entries: NonEmpty<T>): T {
	return entries[0];
}

function isNonEmpty<T>(entries: T[]): entries is NonEmpty<T> {
	return entries.length > 0;
}
```

Narrow a plain array once at the boundary that requires a first entry. The fact then travels in the tuple type. A random numeric index can still be out of bounds to the compiler under `noUncheckedIndexedAccess`. Nonempty tuples prove the first element, not every arbitrary index.

Represent even-length data as pairs.

```ts
type Pairs<T> = [T, T][];
```

For a range, start plus duration can reduce independently mutable fields. It does not by itself exclude negative numbers.

```ts
type DurationMs = number & { readonly __brand: "DurationMs" };

function isDurationMs(value: unknown): value is DurationMs {
	return typeof value === "number" && Number.isFinite(value) && value >= 0;
}

function parseDurationMs(value: unknown): DurationMs {
	if (!isDurationMs(value)) throw new Error("Invalid duration");
	return value;
}

type TimeRange = { start: Date; durationMs: DurationMs };
```

Validate the start date and any application limits at the boundary too. Use an existing duration type when available. Keep a plain number when no duration invariant or semantic mix-up exists. Do not add brands by reflex.

## Simplest total type

An empty array is a valid input to a sum with an identity value.

```ts
const sum = (values: number[]) => values.reduce((total, value) => total + value, 0);
```

Do not strengthen every array. Strengthen when a loose type forces a lie.

```ts
function newestSession(sessions: NonEmpty<Session>): Session {
	return sessions[0];
}
```

When emptiness is an ordinary outcome, return it honestly.

```ts
function maybeNewestSession(sessions: Session[]): Session | undefined {
	return sessions.at(0);
}
```

Avoid `sessions.at(0)!`, `sessions[0] as Session`, and a supposedly impossible throw that merely hides a partial signature.

## Unknown external input

External data starts as `unknown`. Narrow or parse it before use.

```ts
function readCount(input: unknown): number | undefined {
	if (typeof input !== "object" || input === null || !("count" in input)) {
		return undefined;
	}
	return typeof input.count === "number" ? input.count : undefined;
}
```

External sources include RPC payloads, parsed JSON, messages, IPC, files, environment variables, and database responses. Do not turn one of them into `any` to bypass validation. A generated client type may still need runtime validation at a trust boundary.

## Schemas before hand-written guards

Use the schema system the repository already trusts. Let one schema own the runtime check and derive the static type.

```ts
import { z } from "zod";

const UserSchema = z.object({
	id: z.string(),
	role: z.enum(["admin", "member"]),
});

type User = z.infer<typeof UserSchema>;

function parseUser(input: unknown): User {
	return UserSchema.parse(input);
}
```

Use `safeParse` when failure is an expected branch. Use the equivalent inference helper for the installed schema library. Add the real identifier constraints from the domain. Do not maintain a schema, a duplicate interface, and a separate guard with three opportunities to drift. Do not add a new dependency just for this example.

## Avoid unchecked assertions

`data as User` is not validation. Neither is a guard that checks only `id` while claiming both `id` and `name` exist.

```ts
const UserSchema = z.object({ id: z.string(), name: z.string() });
type User = z.infer<typeof UserSchema>;

function parseUser(input: unknown): User {
	return UserSchema.parse(input);
}
```

When a type must come first, check the validator against that complete type.

```ts
type User = { id: string; name: string };

const UserSchema: z.ZodType<User> = z.object({
	id: z.string(),
	name: z.string(),
});
```

Check the installed schema library's API before copying an annotation. Removing `name` from a validator for this required field must fail the typecheck or an explicit schema contract test.

When removing an assertion, identify its cause.

- Add a missing discriminant instead of asserting a variant.
- Narrow an overly wide source type.
- Parse an untyped boundary with its owning schema.
- Use a constructible domain type when the invariant is not represented.
- Use `satisfies` to check a statically known expression, not to validate external data.

If TypeScript cannot express a verified relationship, isolate the smallest assertion at that boundary. Document and test its proof obligation. Do not scatter the same assertion through callers.

## Narrowing order

Prefer these methods in order:

1. Switch or branch on a discriminant.
2. Use `in` for a property that distinguishes variants.
3. Use `typeof` or `instanceof` when they establish the needed runtime fact.
4. Use a sound named type guard.
5. Assert only after actual validation when a better representation is not practical.

```ts
type Shape =
	| { kind: "circle"; radius: number }
	| { kind: "rect"; width: number; height: number };

function area(shape: Shape): number {
	if ("radius" in shape) return Math.PI * shape.radius ** 2;
	return shape.width * shape.height;
}
```

`in` proves property presence. It does not establish a property's type for arbitrary external input without further checks.

## Sound type guards

A guard must verify exactly what it claims. A guard can refine a trusted union by its discriminant.

```ts
function isCircle(shape: Shape): shape is Extract<Shape, { kind: "circle" }> {
	return shape.kind === "circle";
}
```

This input is already `Shape`. The same check is not a complete parser from `unknown`. Prefer a direct discriminant branch when a named guard adds no value.

## Exhaustiveness

In a value-returning switch, return the `never` local from the default arm.

```ts
function area(shape: Shape): number {
	switch (shape.kind) {
		case "circle":
			return Math.PI * shape.radius ** 2;
		case "rect":
			return shape.width * shape.height;
		default: {
			const _exhaustive: never = shape;
			return _exhaustive;
		}
	}
}
```

For a void switch, preserve statement control flow.

```ts
function draw(shape: Shape): void {
	switch (shape.kind) {
		case "circle":
			drawCircle(shape);
			break;
		case "rect":
			drawRect(shape);
			break;
		default: {
			const _exhaustive: never = shape;
			void _exhaustive;
		}
	}
}
```

Adding another union member makes the `never` assignment fail. This is a compile-time guarantee for the declared union. Boundary validation still protects runtime data.

## Satisfies and literal types

Check a literal expression without asserting away a mismatch.

```ts
type Config = { theme: "dark" | "light"; cols: number };

const config = { theme: "dark", cols: 3 } satisfies Config;
```

Here `config.theme` remains `"dark"`. Contextual typing and the target shape affect inference. Do not claim that every string field remains a literal in every `satisfies` expression. The operator checks types at compile time. It does not parse JSON or prove semantic constraints.

## Boundary validation

Validate once where data enters a trust boundary. Pass a named domain value inward. Do not repeat defensive validation in every internal call.

- For a wire format, follow its documented compatibility rules. Ignore unknown fields only when the existing protocol and parser support that behavior safely.
- For persisted JSON, use a versioned representation and explicit parse-failure handling. Do not silently destroy unreadable user data.
- Keep transport and storage representations private when the domain API has a different meaning.
- Keep parse functions and business logic pure where practical. Keep framework wiring thin.

An option such as `ignoreUnknownFields` belongs to a particular parser API. Check the actual library instead of passing that flag to unrelated JSON code.

## Derived types

When a protocol buffer, OpenAPI specification, GraphQL schema, or migration owns a shape, derive from its generated type.

```ts
import type { ChecksMessage } from "<generated module>";

function renderChecks(summary: Pick<ChecksMessage, "totalCount" | "checks">) {
	return summary.checks.map((check) => check.name);
}
```

Replace the illustrative import with the real generated module. Do not copy its fields into another interface just to satisfy a local function. Reach for `Pick`, `Omit`, `Parameters`, `ReturnType`, `Awaited`, and `typeof` first. A genuinely different domain meaning can deserve a separate type.

## Object arguments

Named arguments prevent same-typed positional values from being swapped silently.

```ts
type OpenFileOptions = {
	uri: string;
	selection: {
		startLineNumber: number;
		startColumn: number;
		endLineNumber: number;
		endColumn: number;
	};
};

openFile({
	uri,
	selection: {
		startLineNumber: 10,
		startColumn: 1,
		endLineNumber: 10,
		endColumn: 1,
	},
});
```

Follow an existing public API rather than wrapping it solely for this rule. Skip new object allocation in a measured hot path when it matters. Examples include per-frame rendering, tokenization, and parsing. Do not claim an allocation bottleneck without measurement.

## Real tests and diagnostics

Run the framework's actual test primitives. Check resource disposal and leaks when the runtime exposes those checks. A mocked UI state does not prove a running UI. A passing typecheck does not prove a boundary validator rejects malformed input.

Use structured logs with safe request or domain identifiers and actionable failure context. Avoid logging payloads, credentials, or private identifiers unnecessarily. Intentional CLI stdout and stderr follow the command's output contract. Do not replace machine-readable command output with application logging.
