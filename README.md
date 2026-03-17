# Skin + Me — Full-Stack Technical Assessment

## Context

You are joining a team that has been building an online checkout system. A previous developer started implementing a discount code feature but moved to another project before completing it. Your job is to pick up where they left off.

The codebase includes a working checkout API (Flask/Python) and a checkout frontend (React/TypeScript). A partial discount system has been added to the backend with some frontend scaffolding.

**The existing implementation is incomplete and may contain bugs.** You are expected to find and fix issues as well as complete the remaining features.

## Your Tasks

Your task is outlined below.

### Code Review + Bug Fixes + Feature Completion (~4-5 hours)

The discount system has some issues and missing pieces. This task combines a code review, bug fixes, and feature completion.

**Code review:** A specific commit has been made to this repository containing the initial implementation of the discount system. Review that commit as you would a real PR — the commit ID is `27244c2` (also noted in `REVIEW.md`).

Fill in `REVIEW.md` at the repository root with your feedback. Reference file paths and line numbers to identify issues. For each issue you identify, explain:

- What the problem is
- Why it matters
- How you would fix it

**Bug fixes:** The issues you identify in your review (and any others you find) should be fixed in code. Write tests that demonstrate the bugs and verify your fixes.

**Feature completion:**

- Complete the "remove discount" endpoint (currently returns 501)
- Wire up the frontend discount component to the API
- Display discount feedback (success/error messages) to the user
- Ensure discounts are reflected in the checkout totals on the frontend

See the **Discount System** section below for business rules your implementation must respect.

---

## Discount System

### Constraints

The following is a list of general rules and business logic that you will need to consider as you design your solution.

- Customers MUST use a discount code to trigger the discount.
- Discount codes MUST be unique.
- Applying a discount SHOULD never allow a customer's order to have a negative balance.
- Customers SHOULD only be allowed to use one discount at a time.
- Changing a discount code SHOULD apply and validate the new discount.
- Discounts SHOULD be revalidated on placing an order.

### Supported Discount Types (already modelled)

- **Percentage-based** — e.g. 10% off the order subtotal
- **Fixed amount** — e.g. £5.00 off the order total

### Future Capabilities (context only — do not build)

> [!IMPORTANT]
> You are not expected to build these features! They provide context for you to think about as you design your solution.

#### Discount Management

- See a list of active discount codes.
- See the discount code used on an order.
- Be able to create new discount codes.
- Be able to define how much discount should be applied.
- Be able to manage the discount validation rules.
- Be able to manage custom error messages for invalid discounts.
- Be able to manage custom success messages for valid discounts.

#### Discount Application and Validation

- Apply a conditional discount based on a minimum order value.
- Apply a conditional discount based on specific products.
- Limit the number of times a discount code can be used.
- Limit use of a discount code after an expiry date.
- Limit use of a discount code for people with a specific email address.

---

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Node.js 20+ (see `front-end/.nvmrc`)
- Python 3.12+ (if running the backend locally)

### Running the Project

```bash
# Back-end
cd back-end
make docker-init
make docker-dev

# In another terminal:
make docker-reset-db
make docker-seed-db

# Front-end
cd front-end
npm install
npm run dev
```

### Running Tests

```bash
# Back-end
make docker-test

# Front-end
npm test
```

### Available Seed Data

The following discount codes are seeded for development:

| Code | Type | Amount | Notes |
|---|---|---|---|
| `WELCOME10` | Percentage | 10% off | Active, expires 2030 |
| `FLAT500` | Fixed | £5.00 off | Active, no expiry |
| `EXPIRED2024` | Percentage | 15% off | Expired (Jan 2024) |
| `MAXEDOUT` | Fixed | £3.00 off | Usage limit reached |

The seeded product (Niacinamide-powered night cream) has a unit price of **1999p** (£19.99).

---

## Time Estimate

We expect this assessment to take **4-5 hours**. Please do not spend significantly more than this. If you run out of time, leave comments or pseudocode explaining what you would do next.

## AI Tool Usage

We expect that engineers use AI tools in their daily work. You are welcome to use any AI tools (Copilot, ChatGPT, Claude, Cursor, etc.) during this assessment.

However, you **must**:

1. Disclose which AI tools you used
2. Briefly describe how you used them (e.g. "used Copilot for autocompletion", "asked ChatGPT to explain SQLAlchemy 2.0 migration")
3. Add this to a section titled **AI Usage** at the bottom of your `REVIEW.md`

We value engineers who use AI effectively as a tool, not as a replacement for understanding.

## Further Guidance

Please aim at making a strong submission that reflects well on your knowledge and abilities. The following is a list of themes we will use to assess your work:

- **Feature completion and code quality** — Working features, follows existing patterns, tested, clean commits
- **Bug finding and fixing** — Found and fixed issues, wrote tests proving the bugs and verifying fixes
- **Code review quality** — Identified issues, quality of feedback, constructive tone
- **AI transparency** — Honest disclosure, specific usage description, evidence of judgment

## How to Submit

- Clone the repository to your development machine.
- Create a private repository in your own GitHub account.
- Please commit often (and don't squash); this will help us better understand your progress and reasoning.
- One pull request is sufficient.
- Add the reviewers as collaborators on your repository on GitHub.
