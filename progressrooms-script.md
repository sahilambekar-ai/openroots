# ProgressRooms.com

## Complete Product, Architecture, Database, Payment, Website and Development Specification

---

# 1. PROJECT OVERVIEW

Build a production-ready multi-tenant SaaS application called:

# ProgressRooms

Primary domain:

```text
https://progressrooms.com
```

ProgressRooms is a platform for teachers, instructors, trainers, coaches, and studios who conduct scheduled classes, sessions, workshops, or training programs.

The platform should be industry-agnostic.

Supported use cases may include:

* Yoga teachers
* Aerial yoga instructors
* Dance studios
* Music teachers
* Guitar instructors
* Meditation teachers
* Fitness trainers
* Personal trainers
* Art instructors
* Language teachers
* Coaching businesses
* Mentors
* Nursing training providers
* Professional training organizations
* Workshop organizers
* Small academies

The system should not contain business logic specific to any one industry.

The core architecture must support both:

1. Independent individual teachers.
2. Studios or organizations with multiple instructors.

Internally, both must use the same organization-based architecture.

---

# 2. PRODUCT VISION

ProgressRooms should become an operating platform for businesses that conduct instructor-led sessions.

The platform combines:

```text
Teacher / Studio Management
+
Session Management
+
Scheduling
+
Student Management
+
Payments
+
Public Class Discovery
+
Teacher Public Websites
+
Video Meeting Integration
+
Future AI Features
```

The platform should be capable of growing into a much larger SaaS ecosystem without requiring a fundamental rewrite.

---

# 3. CORE ARCHITECTURAL PRINCIPLE

The system must be multi-tenant.

The core hierarchy:

```text
ProgressRooms Platform
│
├── Super Admin
│
├── Organization / Teacher Business
│      │
│      ├── Owner
│      ├── Admin
│      ├── Teachers / Instructors
│      │
│      ├── Class Types
│      ├── Sessions
│      ├── Schedules
│      ├── Class Occurrences
│      ├── Students
│      ├── Payments
│      └── Website
│
└── Platform Services
```

An independent teacher should internally be represented as:

```text
Organization
+
One Owner
+
One Instructor
```

A studio should internally be represented as:

```text
Organization
+
Multiple Members
+
Multiple Teachers
+
Multiple Sessions
```

Do not create separate database architectures for individual teachers and studios.

---

# 4. TERMINOLOGY

For simplicity in the product UI and documentation, the primary customer can be referred to as:

```text
Teacher
```

However, internally the architecture must support:

```text
Teacher
Studio
Academy
Organization
Business
```

The technical entity should remain:

```text
Organization
```

---

# 5. USER TYPES

The application contains four major user categories.

## 5.1 Super Admin

The ProgressRooms platform owner.

Capabilities:

* Manage all organizations
* Manage all teachers
* Manage all students
* View subscriptions
* View platform revenue
* Manage plans
* Manage website templates
* Manage platform configuration
* Suspend organizations
* View payment information
* View audit logs
* Manage support
* Access platform analytics

---

## 5.2 Organization Owner

The person who creates a ProgressRooms business account.

Capabilities depend on the subscription plan.

Possible capabilities:

* Manage organization
* Add teachers
* Create class types
* Create sessions
* Schedule classes
* Manage students
* View calendar
* Connect payment accounts
* Connect Zoom
* Manage public website
* View revenue
* View enrollments

---

## 5.3 Instructor / Teacher

A teacher can be assigned to sessions.

Capabilities may include:

* View assigned sessions
* View personal calendar
* View students
* Mark attendance
* Conduct classes
* Access meeting links

Teachers should only access resources assigned to them unless additional permissions are granted.

---

## 5.4 Student

Students interact with teachers and sessions.

Students can:

* Create account
* Verify email
* Browse public teacher sessions
* Purchase sessions
* View enrolled sessions
* View upcoming classes
* Join online classes
* View class history
* Receive reminders
* Browse additional sessions from teachers they follow/enroll with

---

# 6. SUBSCRIPTION PLAN SYSTEM

The platform must implement a plan/subscription system for teachers/organizations.

Initial plan structure:

## Plan 1: Starter

Free trial plan.

Suggested duration:

```text
30 days
```

Purpose:

Allow teachers to experience the platform.

---

## Plan 2: Core

Basic paid plan.

For teachers who primarily need:

* Session management
* Scheduling
* Student management
* Calendar
* Payments
* Public profile/class page

---

## Plan 3: Studio

Advanced plan.

For larger teachers/studios requiring:

* Advanced website
* Multiple teachers
* More customization
* Additional business features

---

## Plan 4: Progress AI

Coming Soon.

Do not implement full AI functionality in the initial version.

However, database and product architecture should reserve support for this plan.

Possible future AI features:

* AI website generation
* AI class descriptions
* AI schedule suggestions
* AI student insights
* AI marketing content
* AI assistant for teachers
* AI analytics
* AI communication automation

Display this plan as:

```text
Coming Soon
```

Do not allow checkout yet.

---

# 7. PLAN NAMING

Use the following initial names:

| Tier     | Name        | Status      |
| -------- | ----------- | ----------- |
| Free     | Starter     | Active      |
| Basic    | Core        | Active      |
| Advanced | Studio      | Active      |
| AI       | Progress AI | Coming Soon |

The plan system must be database-driven.

Do not hardcode plan logic throughout the application.

Create:

```text
plans
plan_features
organization_subscriptions
```

The frontend should determine available features through feature entitlements.

Example:

```text
feature: advanced_website

Starter → false
Core → false
Studio → true
Progress AI → future
```

---

# 8. PLAN FEATURE ARCHITECTURE

Do not hardcode conditions like:

```javascript
if (plan === "advanced")
```

Instead implement a feature entitlement system.

Example:

```text
Plan
   │
   └── Plan Features
            │
            ├── max_teachers
            ├── max_students
            ├── website_access
            ├── advanced_website
            ├── custom_domain
            ├── zoom_integration
            └── ai_features
```

Example database:

```text
plans

id
name
slug
description
price
currency
billing_interval
status
is_public
created_at
updated_at
```

---

## plan_features

```text
id

plan_id

feature_key

feature_value

created_at
updated_at
```

Example:

```text
plan: studio

feature_key: advanced_website
feature_value: true
```

Or:

```text
feature_key: max_teachers
feature_value: 10
```

Use JSONB only where appropriate. Prefer typed feature values where possible.

---

# 9. ORGANIZATION SUBSCRIPTION

Create:

```text
organization_subscriptions
```

Fields:

```text
id

organization_id
plan_id

status

starts_at
ends_at

trial_starts_at
trial_ends_at

cancelled_at

payment_provider

provider_subscription_id

created_at
updated_at
```

Possible statuses:

```text
TRIAL
ACTIVE
PAST_DUE
EXPIRED
CANCELLED
SUSPENDED
```

Important:

The initial teacher subscription plan may eventually use recurring payments.

However, do not confuse:

```text
Teacher's ProgressRooms subscription
```

with:

```text
Student purchasing a teacher's class/session.
```

These are completely separate payment domains.

---

# 10. PUBLIC TEACHER PAGE

Every teacher/organization should receive a public page.

URL format:

```text
progressrooms.com/{organization_slug}
```

Example:

```text
progressrooms.com/john-cena-yoga
```

Do not use:

```text
progressrooms.com/johncena.com
```

The public page should be server-side rendered.

---

# 11. DEFAULT PUBLIC PAGE

Available for:

* Starter
* Core
* Studio

The default page is a simple single-page public profile.

It should display:

```text
Teacher / Studio Name

Profile Image

Short Description

Available Class Types

Available Sessions

Session Details

Schedule

Pricing

Prerequisites

Enroll / Buy Button
```

The page should intentionally remain simple.

The primary goal:

```text
Discover Teacher
↓
Explore Sessions
↓
Select Session
↓
Login / Signup
↓
Pay
↓
Become Student
```

---

# 12. PUBLIC SESSION DISCOVERY

When someone visits:

```text
progressrooms.com/{organization_slug}
```

They should see available sessions.

Example:

```text
John's Guitar Academy

Available Classes

────────────────────

Beginner Guitar

Group Class

₹2,000 / Month

[ View Details ]


Advanced Guitar

Group Class

₹3,500 / Month

[ View Details ]


Private Guitar

1-on-1

₹1,000 / Session

[ View Details ]
```

Sessions displayed publicly must respect:

```text
session visibility
session status
organization subscription entitlements
```

Only active and publicly visible sessions should be displayed.

---

# 13. SESSION CREATION

When teachers create a session, they should provide sufficient information for public display.

Session creation form should support:

## Basic Information

```text
Session Name

Class Type

Short Description

Full Description
```

---

## Session Type

Examples:

```text
GROUP
ONE_TO_ONE
WORKSHOP
PROGRAM
```

Keep extensible.

---

## Instructor Assignment

Allow:

* Primary instructor
* Secondary instructor
* Substitute instructor

---

## Session Details

```text
Capacity

Minimum Age

Maximum Age

Skill Level

Duration

Language
```

Not every field should be mandatory.

---

## Schedule

Teacher should define:

```text
Days

Start Time

End Time

Timezone

Start Date

End Date
```

---

## Pricing

Teacher must be able to define:

```text
Price

Currency

Pricing Type
```

Possible pricing types:

```text
ONE_TIME
MONTHLY
PACKAGE
PER_SESSION
CUSTOM
```

Initial implementation can support the most important pricing models.

---

## Prerequisites

Teacher should be able to provide:

```text
Prerequisites

Required Equipment

Preparation Instructions

Additional Notes
```

Example:

```text
Please bring your own yoga mat.

Suitable for beginners.

No prior experience required.
```

These details should automatically appear on the public session page.

---

# 14. SESSION DETAIL PAGE

When a visitor clicks a session, they should see a dedicated SSR page.

Example:

```text
progressrooms.com/{organization_slug}/sessions/{session_slug}
```

Example:

```text
progressrooms.com/john-guitar/sessions/beginner-guitar
```

The page should be server-side rendered.

Page contents:

```text
Session Title

Hero Image

Description

Teacher / Instructor

Class Type

Skill Level

Schedule

Duration

Start Date

End Date

Prerequisites

Required Equipment

Available Seats

Pricing

[ Enroll Now ]
```

---

# 15. STUDENT ENROLLMENT FLOW

The enrollment flow must be carefully designed.

## Step 1

Visitor discovers teacher page.

```text
progressrooms.com/john-guitar
```

---

## Step 2

Visitor selects a session.

---

## Step 3

Visitor clicks:

```text
Enroll Now
```

---

## Step 4

Check authentication.

If not logged in:

```text
Login / Signup
```

---

# 16. STUDENT AUTHENTICATION

Initial authentication flow should support email OTP verification.

Suggested flow:

```text
Enter Email
      ↓
Send OTP
      ↓
Verify OTP
      ↓
Account Created / Logged In
```

Do not require a complicated password-based onboarding initially.

Email OTP should establish:

```text
Verified Student Identity
```

Architecture should still allow future authentication methods:

```text
Password

Google OAuth

Phone OTP

Apple Login
```

---

# 17. POST-LOGIN ENROLLMENT FLOW

After successful login:

The system should return the student to the previously selected session.

Do not make the user manually navigate back.

Persist the intended action.

Example:

```text
Student clicked:

Enroll Beginner Guitar

Not logged in

↓ Login

After login

↓ Automatically return

Beginner Guitar

[ Proceed to Payment ]
```

---

# 18. PAYMENT FLOW

Payment provider:

```text
Razorpay
```

The complete student purchase flow:

```text
Public Session Page
        ↓
Enroll Now
        ↓
Authentication Check
        ↓
Login / OTP Verification
        ↓
Student Account Created
        ↓
Order Created
        ↓
Price Calculated
        ↓
Razorpay Checkout
        ↓
Payment Success
        ↓
Webhook Verification
        ↓
Payment Recorded
        ↓
Enrollment Activated
        ↓
Student Dashboard Updated
        ↓
Confirmation Email
```

Enrollment must not be activated merely because the frontend says payment succeeded.

The backend must verify payment.

Prefer:

```text
Razorpay webhook
```

as the authoritative payment confirmation mechanism.

---

# 19. PAYMENT ARCHITECTURE

Create a separate commerce/payment domain.

Suggested entities:

```text
orders

order_items

payments

payment_attempts

refunds
```

Do not mix payment data directly into session enrollment tables.

---

# 20. ORDER MODEL

```text
orders

id

organization_id
student_id

status

subtotal_amount
discount_amount
tax_amount
total_amount

currency

payment_status

created_at
updated_at
```

Order statuses:

```text
PENDING
PAYMENT_PENDING
PAID
FAILED
CANCELLED
REFUNDED
PARTIALLY_REFUNDED
```

---

# 21. ORDER ITEMS

```text
order_items

id

order_id

purchasable_type
purchasable_id

name_snapshot

quantity

unit_price

total_price

metadata

created_at
```

This architecture allows future purchases of:

```text
Sessions

Packages

Memberships

Workshops

Digital Products
```

---

# 22. PAYMENT MODEL

```text
payments

id

organization_id
student_id
order_id

provider

provider_payment_id

provider_order_id

amount

currency

status

payment_method

provider_response

paid_at

created_at
updated_at
```

Possible providers:

```text
RAZORPAY
```

Future:

```text
STRIPE
PAYPAL
OTHER
```

---

# 23. PAYMENT SECURITY

Never trust frontend payment success.

Payment completion should follow:

```text
Razorpay
       │
       ▼
Webhook Received
       │
       ▼
Verify Signature
       │
       ▼
Verify Amount
       │
       ▼
Verify Order
       │
       ▼
Mark Payment Paid
       │
       ▼
Activate Enrollment
```

Webhook processing must be idempotent.

Repeated webhooks must not create duplicate enrollments.

---

# 24. TEACHER PAYMENT ACCOUNT MODEL

The platform architecture must consider how money flows.

Student payments belong to teachers/organizations.

The system should support future payment account connections.

Possible architecture:

```text
Organization
      │
      └── Payment Account
               │
               └── Razorpay Account / Route / Partner Account
```

Create:

```text
organization_payment_accounts
```

Fields:

```text
id

organization_id

provider

provider_account_id

status

configuration

created_at
updated_at
```

Do not hardcode the assumption that all money permanently enters the platform owner's account.

Payment settlement architecture must be designed separately according to Razorpay's supported marketplace/platform products and compliance requirements.

---

# 25. STUDENT ENROLLMENT

After successful payment:

Create or activate:

```text
session_enrollment
```

Example:

```text
Student A

Session:
Beginner Guitar

Enrollment Status:
ACTIVE

Payment:
PAID

Access:
Enabled
```

Suggested fields:

```text
id

organization_id
student_id
session_id

order_id

status

access_starts_at
access_ends_at

remaining_sessions

created_at
updated_at
```

---

# 26. SUBSCRIPTION-LIKE SESSION ACCESS

This is not necessarily an automatic recurring subscription.

Instead, the platform should support access periods.

Examples:

```text
Monthly Access
```

or:

```text
10 Class Package
```

or:

```text
Access Until Program End
```

Create:

```text
enrollment_access_type
```

Possible values:

```text
DATE_RANGE

NUMBER_OF_CLASSES

PROGRAM_DURATION

UNLIMITED
```

---

# 27. MONTHLY ACCESS EXAMPLE

Student purchases:

```text
Yoga Monthly Plan

₹2,000

Access:
30 Days
```

Enrollment:

```text
Starts:
September 1

Ends:
September 30
```

The system should schedule reminder notifications before expiration.

Example:

```text
7 days remaining

3 days remaining

1 day remaining

Expired
```

---

# 28. NUMBER OF SESSION ACCESS

Example:

```text
10 Yoga Classes

₹3,000
```

Enrollment:

```text
Remaining Classes:
10
```

After attendance:

```text
Remaining Classes:
9
```

When the remaining count reaches thresholds:

```text
3 Classes Remaining

1 Class Remaining

0 Classes Remaining
```

The notification system should support reminders.

---

# 29. ENROLLMENT RENEWAL

When an enrollment is about to expire:

Send notification:

```text
Your Beginner Guitar enrollment expires in 3 days.

Renew to continue attending classes.
```

Student clicks:

```text
Renew
```

The system creates a new order.

After payment:

Extend or create a new enrollment period.

Maintain payment history.

---

# 30. NOTIFICATION SYSTEM

Initial notification channels:

```text
IN_APP

EMAIL
```

Future:

```text
WHATSAPP

SMS

PUSH
```

Do not tightly couple notification logic to email.

Use a generic notification abstraction.

---

# 31. NOTIFICATION EVENTS

Potential events:

```text
STUDENT_ENROLLED

PAYMENT_SUCCESS

PAYMENT_FAILED

CLASS_REMINDER

CLASS_CANCELLED

CLASS_RESCHEDULED

ENROLLMENT_EXPIRING

ENROLLMENT_EXPIRED

NEW_SESSION_AVAILABLE
```

---

# 32. NOTIFICATION PREFERENCE ARCHITECTURE

Future support:

```text
user_notification_preferences
```

Allow users to eventually control:

```text
Email notifications

WhatsApp notifications

Class reminders

Marketing notifications
```

---

# 33. STUDENT DASHBOARD

The student dashboard should remain simple.

Navigation:

```text
Dashboard

My Classes

Explore

Payments

Profile
```

---

## Dashboard

Display:

```text
Upcoming Class

Next Class

Session

Instructor

Date

Time

[ Join Class ]
```

---

## My Classes

Display all active enrollments.

Example:

```text
My Classes

Beginner Guitar
Active
8 Classes Remaining

Advanced Guitar
Expires September 30
```

---

## Explore

Students should see other available sessions from organizations where appropriate.

Initial implementation:

Students primarily see sessions from teachers/studios where they have already interacted or the public website they visit.

Future marketplace discovery can be added later.

---

# 34. CLASS ACCESS CONTROL

Students should only see meeting links for classes they are authorized to attend.

Before displaying:

```text
Join Class
```

Validate:

```text
Student
      │
      ▼
Active Enrollment
      │
      ▼
Correct Session
      │
      ▼
Valid Access Period
      │
      ▼
Meeting Access Allowed
```

Never expose all Zoom URLs publicly.

---

# 35. DEFAULT WEBSITE SYSTEM

Every organization gets a default public presence.

Available on:

```text
Starter

Core

Studio
```

Default URL:

```text
progressrooms.com/{organization_slug}
```

This page is generated automatically.

Teachers manage content from their dashboard.

---

# 36. DEFAULT WEBSITE CONTENT

Teacher can manage:

```text
Organization Name

Profile Image

Description

Short Introduction

Location

Contact Information

Social Links
```

Public page automatically displays:

```text
About

Explore Classes

Sessions

Contact
```

Do not allow complex page building for Starter/Core plans.

---

# 37. ADVANCED WEBSITE FEATURE

Available only on:

```text
Studio Plan
```

The teacher can choose a professionally designed website template.

Initial number of templates:

```text
3 templates
```

Future:

```text
5+ templates
```

---

# 38. IMPORTANT WEBSITE TEMPLATE PRINCIPLE

These are not drag-and-drop websites.

Do not build a Wix-like page builder.

The template structure must remain fixed.

Example:

```text
Template 1

Hero
About
Images
Explore Classes
Testimonials
Location
Contact
```

Teacher cannot:

* Move arbitrary sections
* Change HTML structure
* Modify layout architecture

Teacher can modify approved content fields.

---

# 39. ADVANCED WEBSITE CUSTOMIZATION

Teachers may configure:

```text
Logo

Hero Images

Gallery Images

Organization Description

Contact Information

Location

Social Links

Selected Website Sections

Sessions
```

Potential future:

```text
Testimonials

FAQs

Promotional Banner
```

---

# 40. WEBSITE TEMPLATE SYSTEM

Create:

```text
website_templates
```

Fields:

```text
id

name

slug

description

status

preview_image_url

template_version

is_available

created_at
updated_at
```

Template content/layout must be versioned.

Do not store arbitrary template HTML directly in the database.

The application code should render templates.

Database stores:

```text
Template Selection

Configuration

Content

Images

Section Settings
```

---

# 41. ORGANIZATION WEBSITE CONFIGURATION

Create:

```text
organization_websites
```

Fields:

```text
id

organization_id

template_id

website_type

status

configuration

published_at

created_at
updated_at
```

Website types:

```text
DEFAULT

ADVANCED
```

Configuration can contain structured JSON.

Example:

```json
{
  "hero": {
    "title": "Learn Guitar With John",
    "subtitle": "Professional guitar classes",
    "image": "..."
  },
  "contact": {
    "email": "...",
    "phone": "..."
  }
}
```

Validate configuration using template-specific schemas.

Do not allow arbitrary uncontrolled JSON without validation.

---

# 42. WEBSITE TEMPLATE CONTENT MANAGEMENT

The dashboard should dynamically show editable fields depending on the selected template.

Example:

Teacher selects:

```text
Template A
```

Dashboard shows:

```text
Hero Title

Hero Subtitle

Hero Image

About Description

Gallery Images

Contact Number

Email

Location

Social Links
```

Teacher should see a preview.

---

# 43. EXPLORE CLASSES WEBSITE SECTION

All websites should integrate dynamically with the existing session system.

Do not manually create class cards inside website configuration.

Instead:

```text
Website
     │
     ▼
Explore Classes Section
     │
     ▼
Fetch Organization Class Types
     │
     ▼
Fetch Active Public Sessions
```

This ensures that:

When teacher creates a new session:

```text
Session automatically appears
```

When teacher disables a session:

```text
Session automatically disappears
```

No duplicate content management should be required.

---

# 44. WEBSITE ROUTING

Example routes:

```text
/{organization_slug}
```

Default organization website.

Session:

```text
/{organization_slug}/sessions/{session_slug}
```

Potential advanced pages:

```text
/{organization_slug}/about

/{organization_slug}/contact

/{organization_slug}/classes
```

The exact available pages depend on the selected template.

---

# 45. SERVER-SIDE RENDERING

Public organization websites must use SSR.

Reasons:

```text
SEO

Performance

Social Sharing

Search Engine Indexing

Fast Initial Load
```

Do not build public teacher websites as client-only dashboards.

Recommended architecture should support:

```text
SSR

Server Components where applicable

Dynamic Metadata

Open Graph Metadata

Structured SEO Metadata
```

---

# 46. SEO ARCHITECTURE

Each organization should be able to have:

```text
Page Title

Meta Description

Open Graph Image
```

Generate sensible defaults.

Example:

```text
John Guitar Academy | Guitar Classes in Bengaluru
```

Session pages should also have dynamic metadata.

Example:

```text
Beginner Guitar Classes | John Guitar Academy
```

---

# 47. WEBSITE IMAGE MANAGEMENT

Create a reusable media system.

Suggested entity:

```text
media_assets
```

Fields:

```text
id

organization_id

uploaded_by

storage_provider

file_name

file_type

file_size

url

metadata

created_at
```

Future support:

```text
Image optimization

Cropping

WebP conversion

CDN

Image variants
```

Do not store large binary images directly inside PostgreSQL.

---

# 48. CLASS TYPE ARCHITECTURE

Class Types remain organization-specific.

Examples:

```text
Yoga

Aerial Yoga

Guitar

Dance

Meditation
```

Table:

```text
class_types
```

Fields:

```text
id

organization_id

name

slug

description

status

created_at
updated_at
deleted_at
```

---

# 49. SESSION ARCHITECTURE

A session is a product/program offering.

Examples:

```text
Beginner Guitar Group

Advanced Guitar Group

Private Guitar Classes

Weekend Guitar Workshop
```

Fields:

```text
id

organization_id

class_type_id

name

slug

short_description

description

session_type

visibility

status

capacity

minimum_age

maximum_age

skill_level

language

duration_minutes

cover_image_id

created_at
updated_at
deleted_at
```

---

# 50. SESSION PRICING MODEL

Do not store all pricing directly in the session table.

Create:

```text
session_pricing
```

Fields:

```text
id

session_id

name

description

pricing_type

amount

currency

access_type

access_duration_days

included_class_count

status

created_at
updated_at
```

Possible pricing:

```text
ONE_TIME

MONTHLY

PACKAGE

PER_SESSION
```

A session may eventually support multiple pricing options.

Example:

```text
Yoga

Monthly
₹2,000

10 Class Package
₹1,800
```

---

# 51. SESSION PREREQUISITES

Create a structured model or validated content field.

Suggested:

```text
session_requirements
```

Fields:

```text
id

session_id

requirement_type

title

description

is_required

display_order

created_at
updated_at
```

Types:

```text
PREREQUISITE

EQUIPMENT

PREPARATION

NOTE
```

---

# 52. SESSION INSTRUCTOR ASSIGNMENT

Use:

```text
session_instructors
```

Fields:

```text
id

session_id

organization_member_id

role

created_at
updated_at
```

Roles:

```text
PRIMARY

SECONDARY

SUBSTITUTE
```

---

# 53. STUDENT ARCHITECTURE

A student is globally a user.

However, the student can interact with multiple organizations.

Example:

```text
Student A

Yoga Studio → Student

Guitar Academy → Student

Dance Studio → Student
```

Therefore:

Do not create separate student user accounts per organization.

Use:

```text
users
```

and organization-specific relationships.

---

# 54. ORGANIZATION MEMBERSHIP

Use:

```text
organization_members
```

Fields:

```text
id

organization_id

user_id

role

status

joined_at

created_at
updated_at
```

Roles:

```text
OWNER

ADMIN

INSTRUCTOR
```

Student relationships should primarily exist through enrollment rather than forcing every student into organization_members.

However, architecture may allow organization-specific student profiles later.

---

# 55. STUDENT PROFILE WITHIN ORGANIZATION

Create:

```text
organization_students
```

Fields:

```text
id

organization_id

user_id

status

notes

created_at
updated_at
```

This allows a student to have an organization-specific relationship.

Example:

```text
Student globally:
Sahil

Organization:
John Guitar Academy

Status:
Active Student
```

---

# 56. SESSION ENROLLMENT

Create:

```text
session_enrollments
```

Fields:

```text
id

organization_id

organization_student_id

session_id

pricing_id

order_id

status

access_type

access_starts_at

access_ends_at

included_class_count

remaining_class_count

created_at
updated_at
```

Statuses:

```text
PENDING

ACTIVE

PAUSED

EXPIRED

CANCELLED

COMPLETED
```

---

# 57. SCHEDULING ARCHITECTURE

Critical distinction:

```text
Session
≠
Individual Class
```

Example:

```text
Session:

Beginner Guitar Group
```

Schedule:

```text
Monday
Wednesday

6 PM – 7 PM
```

Individual occurrences:

```text
September 7 – 6 PM

September 9 – 6 PM

September 14 – 6 PM
```

---

# 58. SESSION SCHEDULE RULES

Create:

```text
session_schedule_rules
```

Fields:

```text
id

organization_id

session_id

recurrence_type

day_of_week

start_time

end_time

timezone

effective_from

effective_until

is_active

created_at
updated_at
```

Future support:

```text
RRULE
```

But avoid prematurely implementing extremely complex recurrence systems unless required.

---

# 59. CLASS OCCURRENCES

Create:

```text
class_occurrences
```

Fields:

```text
id

organization_id

session_id

schedule_rule_id

original_start_at

original_end_at

actual_start_at

actual_end_at

status

meeting_provider

meeting_id

meeting_join_url

notes

created_at
updated_at
```

Statuses:

```text
SCHEDULED

IN_PROGRESS

COMPLETED

CANCELLED

POSTPONED

RESCHEDULED
```

---

# 60. CLASS CHANGE HISTORY

Create:

```text
class_occurrence_changes
```

Fields:

```text
id

class_occurrence_id

change_type

previous_data

new_data

reason

changed_by

created_at
```

Never destroy original scheduling history.

---

# 61. CALENDAR SYSTEM

Provide:

## Organization Calendar

All organization events.

Filters:

```text
Teacher

Session

Class Type

Status

Date Range
```

---

## Instructor Calendar

Only assigned classes.

---

## Student Calendar

Only accessible enrolled classes.

---

# 62. INSTRUCTOR CONFLICT DETECTION

When scheduling:

Check whether an instructor already has another class.

Example:

```text
Teacher A

Class A
10:00–11:00

Class B
10:30–11:30

Conflict
```

Initial version:

Show warning.

Do not necessarily block scheduling initially.

---

# 63. ZOOM / VIDEO ARCHITECTURE

Zoom should be an integration provider.

Do not tightly couple the system only to Zoom.

Use:

```text
meeting_provider
```

Possible values:

```text
ZOOM

GOOGLE_MEET

OTHER
```

Initial implementation:

```text
ZOOM
```

---

# 64. INTEGRATION SYSTEM

Create:

```text
organization_integrations
```

Fields:

```text
id

organization_id

provider

account_identifier

encrypted_credentials

configuration

status

created_at
updated_at
```

Credentials must be encrypted.

Never store tokens in plaintext.

---

# 65. MEETING GENERATION

Individual class occurrences may generate meetings.

Flow:

```text
Class Occurrence Created
        ↓
Determine Instructor
        ↓
Determine Connected Account
        ↓
Call Zoom API
        ↓
Create Meeting
        ↓
Store Meeting Metadata
```

Students see:

```text
Join Class
```

Teachers see:

```text
Start / Manage Class
```

---

# 66. ATTENDANCE

Create:

```text
attendance_records
```

Fields:

```text
id

organization_id

class_occurrence_id

organization_student_id

status

marked_by

marked_at

notes

created_at
updated_at
```

Statuses:

```text
PRESENT

ABSENT

LATE

EXCUSED
```

Attendance may affect:

```text
remaining_class_count
```

for class packages.

This logic must be transactional and carefully designed.

---

# 67. CLASS PACKAGE CONSUMPTION

For students with:

```text
10 Classes Package
```

Attendance should potentially consume one class.

Flow:

```text
Remaining Classes: 10

Student Attends

↓ Attendance marked PRESENT

Remaining Classes: 9
```

Do not blindly decrement multiple times.

Use transactional/idempotent logic.

---

# 68. TEACHER DASHBOARD

Main navigation:

```text
Dashboard

Calendar

Class Types

Sessions

Classes

Teachers

Students

Enrollments

Payments

Website

Integrations

Settings
```

Visibility depends on plan and role.

---

# 69. DASHBOARD FEATURE GATING

Feature availability must be determined by:

```text
Organization Subscription
        +
Plan Entitlements
        +
User Role
```

Example:

```text
Website
```

Starter:

```text
Default website only
```

Core:

```text
Default website only
```

Studio:

```text
Advanced templates enabled
```

Progress AI:

```text
Future AI capabilities
```

---

# 70. WEBSITE DASHBOARD

For eligible Studio plan users:

Navigation:

```text
Website

Choose Template

Customize Content

Images

Preview

Publish
```

---

# 71. TEMPLATE SELECTION

Initial templates:

```text
Template A

Template B

Template C
```

These can be internally referred to as:

```text
AI Website Templates
```

However, initial implementation does not need actual generative AI.

Templates should be:

* Professionally designed
* Responsive
* Fixed structure
* Dynamic content driven

---

# 72. TEMPLATE CUSTOMIZATION RULES

Teachers can modify:

```text
Images

Text Content

Contact Details

Location

Social Links

Session Data
```

Teachers cannot:

```text
Drag sections arbitrarily

Modify page layout

Edit template code

Create arbitrary page structures
```

This is intentional.

Do not build a page builder.

---

# 73. TEMPLATE SECTION ARCHITECTURE

Templates may contain:

```text
Hero

About

Gallery

Explore Classes

Testimonials

Location

Contact
```

Each template defines:

```text
Available Sections

Section Order

Editable Fields

Validation Rules
```

The database configuration must follow the selected template schema.

---

# 74. PUBLIC WEBSITE SSR REQUIREMENT

All public pages must be server-side rendered.

Important pages:

```text
Organization Home

Session Listing

Session Detail

About

Contact
```

Benefits:

```text
SEO

Fast Loading

Social Sharing

Search Engine Indexing
```

Do not make public websites depend entirely on authenticated client-side APIs.

---

# 75. PUBLIC ROUTING COLLISION MANAGEMENT

Because public organizations use:

```text
progressrooms.com/{slug}
```

Reserved slugs must be protected.

Examples:

```text
admin

login

signup

dashboard

api

pricing

sessions

about

contact

settings
```

Create a reserved slug validation system.

Organization slugs must be unique.

---

# 76. CUSTOM DOMAIN SUPPORT

Not required in MVP.

However, future Studio plan may support:

```text
www.johnguitar.com
```

pointing to the ProgressRooms website.

Prepare architecture but do not implement DNS management initially.

Future table:

```text
organization_domains
```

---

# 77. SUPER ADMIN DASHBOARD

Super admin navigation:

```text
Dashboard

Organizations

Teachers

Students

Plans

Subscriptions

Payments

Website Templates

Platform Analytics

Support

Audit Logs

Settings
```

---

# 78. SUPER ADMIN CAPABILITIES

Super admin can:

```text
View all organizations

Search organizations

Suspend organization

Activate organization

View subscriptions

Change plans manually

View payment records

Manage templates

Manage plans

View platform analytics
```

Super admin must not bypass audit logging.

Administrative actions should be logged.

---

# 79. PLATFORM ANALYTICS

Future analytics architecture should support:

```text
Total Organizations

Active Organizations

Trial Organizations

Total Teachers

Total Students

Total Sessions

Upcoming Classes

Classes Completed

Platform GMV

Platform Revenue

Active Subscriptions
```

Do not over-engineer analytics in MVP.

Ensure data model allows future aggregation.

---

# 80. AUTHENTICATION VS AUTHORIZATION

Maintain strict separation.

Authentication:

```text
Who is the user?
```

Authorization:

```text
What is the user allowed to do?
```

Use:

```text
users

organization_members

roles

permissions
```

Authorization must be enforced server-side.

Frontend hiding of buttons is not authorization.

---

# 81. ROLE ARCHITECTURE

Initial roles:

```text
SUPER_ADMIN

OWNER

ADMIN

INSTRUCTOR

STUDENT
```

Avoid excessive permission complexity in MVP.

However, design a future RBAC extension.

Potential:

```text
roles

permissions

role_permissions
```

---

# 82. NOTIFICATION ARCHITECTURE

Create:

```text
notifications
```

Fields:

```text
id

user_id

organization_id

event_type

channel

title

message

metadata

status

read_at

sent_at

created_at
```

Channels:

```text
IN_APP

EMAIL

WHATSAPP

SMS

PUSH
```

Initial active channels:

```text
IN_APP

EMAIL
```

---

# 83. NOTIFICATION JOB SYSTEM

Do not send scheduled reminders directly inside API requests.

Use background jobs.

Examples:

```text
Upcoming class reminder

Enrollment expiry reminder

Payment confirmation

Class cancellation notification
```

The system should have a background job architecture.

Potential future worker:

```text
Notification Worker

Scheduling Worker

Meeting Generation Worker
```

---

# 84. EMAIL REMINDERS

Examples:

```text
Your class starts in 1 hour.
```

```text
Your enrollment expires in 3 days.
```

```text
You have 2 classes remaining.
```

Emails should be generated through reusable templates.

---

# 85. WHATSAPP FUTURE SUPPORT

Do not implement immediately.

But notification architecture must support it.

Future integration:

```text
WhatsApp Business API
```

Use event-based notification architecture so WhatsApp can subscribe to existing events.

Do not create separate business logic later.

---

# 86. PAYMENT REMINDERS

Students should receive reminders based on enrollment type.

Examples:

## Date-Based Access

```text
7 days before expiration

3 days before expiration

1 day before expiration
```

---

## Class Package

```text
3 classes remaining

1 class remaining

0 classes remaining
```

---

# 87. PAYMENT RENEWAL FLOW

Student:

```text
Enrollment Expiring
```

Clicks:

```text
Renew
```

System:

```text
Create Order

Create Razorpay Payment

Verify Payment

Extend Enrollment
```

---

# 88. RAZORPAY WEBHOOK REQUIREMENTS

Implement:

```text
Webhook Signature Validation

Idempotency

Retry Handling

Logging

Failure Monitoring
```

Create:

```text
payment_webhook_events
```

Fields:

```text
id

provider

event_id

event_type

payload

status

processed_at

error_message

created_at
```

Prevent duplicate event processing.

---

# 89. DATABASE ARCHITECTURE

Primary database:

```text
PostgreSQL
```

Use:

```text
UUID Primary Keys

Foreign Keys

TIMESTAMPTZ

JSONB where justified

Indexes

Constraints

Transactions
```

---

# 90. CORE DATABASE TABLES

Authentication:

```text
users

user_auth_methods

user_sessions
```

Platform:

```text
platform_admins
```

Organizations:

```text
organizations

organization_members

organization_students

organization_settings
```

Plans:

```text
plans

plan_features

organization_subscriptions
```

Class Management:

```text
class_types

sessions

session_instructors

session_pricing

session_requirements
```

Scheduling:

```text
session_schedule_rules

class_occurrences

class_occurrence_changes
```

Enrollment:

```text
session_enrollments
```

Attendance:

```text
attendance_records
```

Payments:

```text
orders

order_items

payments

payment_attempts

refunds

payment_webhook_events

organization_payment_accounts
```

Website:

```text
website_templates

organization_websites

organization_domains

media_assets
```

Integrations:

```text
organization_integrations
```

Notifications:

```text
notifications

notification_preferences
```

System:

```text
audit_logs
```

---

# 91. DATABASE INDEXING

Optimize heavily for organization-scoped queries.

Important indexes:

```text
organization_id

user_id

session_id

class_occurrence_id

actual_start_at

status

student_id
```

Common calendar query:

```sql
WHERE organization_id = ?
AND actual_start_at BETWEEN ? AND ?
ORDER BY actual_start_at
```

Create appropriate composite indexes.

---

# 92. MULTI-TENANT SECURITY

Every organization-scoped entity must contain:

```text
organization_id
```

Where logically appropriate.

Every query must validate:

```text
Authenticated User
        ↓
Organization Membership
        ↓
Role
        ↓
Permission
        ↓
Resource Organization
```

Cross-organization data leakage must be impossible.

---

# 93. SOFT DELETE POLICY

Use soft deletes for important business entities.

Field:

```text
deleted_at
```

Potential:

```text
Organizations

Class Types

Sessions

Media Assets
```

Do not destroy historical payment or audit records.

---

# 94. AUDIT LOGGING

Create:

```text
audit_logs
```

Fields:

```text
id

organization_id

user_id

entity_type

entity_id

action

old_data

new_data

ip_address

created_at
```

Important actions:

```text
Organization Updated

Teacher Added

Session Created

Session Updated

Class Cancelled

Class Rescheduled

Payment Refunded

Plan Changed
```

---

# 95. TIMEZONE STRATEGY

All database timestamps:

```text
TIMESTAMPTZ
```

Store consistently.

Organization has:

```text
timezone
```

Example:

```text
Asia/Kolkata
```

Rules:

```text
Store timestamps correctly.

Render according to user/organization timezone.

Never rely on browser timezone alone.

Never store ambiguous datetime values.
```

---

# 96. API MODULE ARCHITECTURE

Separate backend domains.

Suggested modules:

```text
Auth

Users

Organizations

Memberships

Subscriptions

Plans

Class Types

Sessions

Scheduling

Calendar

Enrollments

Attendance

Payments

Razorpay

Meetings

Integrations

Websites

Media

Notifications

Admin
```

Avoid giant controllers.

Avoid mixing business domains.

---

# 97. FEATURE ENTITLEMENT SERVICE

Implement a centralized entitlement service.

Example:

```text
canUseFeature(
    organization,
    "advanced_website"
)
```

Possible checks:

```text
Subscription Active?

Plan Includes Feature?

Usage Limit Reached?

Organization Status Active?
```

Do not duplicate this logic throughout the codebase.

---

# 98. USAGE LIMIT SYSTEM

Plans may eventually limit:

```text
Number of Teachers

Number of Students

Number of Sessions

Number of Website Templates

Storage
```

Create centralized usage tracking/checking.

Example:

```text
getOrganizationUsage()

checkPlanLimit()
```

---

# 99. BACKGROUND JOBS

The system should support asynchronous jobs.

Initial jobs:

```text
Generate Future Class Occurrences

Send Email Notification

Enrollment Expiry Check

Class Reminder

Payment Processing

Zoom Meeting Creation
```

Do not run expensive recurring logic during user requests.

---

# 100. CLASS OCCURRENCE GENERATION

Recommended approach:

Generate occurrences ahead of time.

Example:

```text
Next 90 days
```

Background job:

```text
Find Active Session Schedule Rules

Generate Missing Class Occurrences

Avoid Duplicates
```

Use uniqueness constraints.

Do not generate infinite future occurrences.

---

# 101. DUPLICATE PREVENTION

Use database constraints.

Example:

A schedule rule should not generate the same occurrence twice.

Consider unique constraint on:

```text
session_id

schedule_rule_id

original_start_at
```

---

# 102. TRANSACTION REQUIREMENTS

Use database transactions for critical flows.

Examples:

## Payment Success

```text
Payment Updated
+
Order Updated
+
Enrollment Activated
+
Notification Created
```

Must be handled safely.

---

## Attendance

```text
Attendance Updated
+
Remaining Class Count Updated
```

Must prevent duplicate consumption.

---

# 103. ERROR HANDLING

Implement:

```text
Structured Errors

Error Codes

Request Logging

Server Error Monitoring

Payment Failure Logging

Integration Failure Logging
```

Do not expose internal stack traces to users.

---

# 104. PUBLIC WEBSITE PERFORMANCE

Public SSR pages should be optimized.

Consider:

```text
Caching

Incremental Regeneration where appropriate

CDN for media

Optimized images

Lazy loading
```

Dashboard data should remain private and authenticated.

---

# 105. SEO REQUIREMENTS

Public pages require:

```text
Dynamic Title

Meta Description

Canonical URL

Open Graph Tags

Twitter Metadata

Structured Data where appropriate
```

Session pages should be indexable.

---

# 106. PROJECT FOLDER STRUCTURE

Maintain clean project organization.

Suggested high-level structure:

```text
/project-root

    /apps
        /web
        /api

    /packages
        /database
        /shared
        /ui

    /docs

    /tests

    /scripts

    /infrastructure
```

Actual structure can vary based on technology choices.

The architecture should clearly separate:

```text
Application Code

Database

Documentation

Tests

Scripts

Infrastructure
```

---

# 107. PROJECT DOCUMENTATION FOLDER

Create:

```text
/docs
```

Every major implementation phase must produce documentation.

Suggested structure:

```text
/docs

    /01-product
    /02-architecture
    /03-database
    /04-api
    /05-auth
    /06-payments
    /07-scheduling
    /08-websites
    /09-testing
    /10-deployment
```

---

# 108. REQUIRED DOCUMENTS

The following documents must exist.

```text
01-product-overview.md

02-domain-model.md

03-user-roles.md

04-user-flows.md

05-er-diagram.md

06-database-schema.md

07-api-specification.md

08-auth-authorization.md

09-scheduling-engine.md

10-payment-architecture.md

11-razorpay-integration.md

12-subscription-system.md

13-website-system.md

14-multi-tenancy.md

15-security.md

16-testing-strategy.md

17-deployment.md
```

Documentation must evolve with the implementation.

---

# 109. TEST PROJECT FOLDER

Create:

```text
/tests
```

Structure:

```text
/tests

    /unit

    /integration

    /e2e

    /fixtures

    /seed-data

    /scenarios
```

---

# 110. TEST SCENARIOS

Create detailed test scenarios.

Examples:

```text
Super Admin Login

Organization Owner Signup

Teacher Invitation

Teacher Login

Student OTP Login

Session Creation

Session Scheduling

Class Rescheduling

Class Cancellation

Student Enrollment

Razorpay Payment

Payment Failure

Payment Webhook Retry

Enrollment Expiry

Class Package Exhaustion

Website Template Selection

Public Session Discovery
```

---

# 111. TEST USER ACCOUNTS

Create a test credentials document:

```text
/docs/09-testing/test-accounts.md
```

Example accounts:

## Super Admin

```text
Email:
admin@test.progressrooms.local
```

---

## Teacher / Owner

```text
Email:
owner@yogastudio.test
```

---

## Multi-Teacher Studio

```text
Owner:
studio@test.progressrooms.local

Instructor A:
teacher1@test.progressrooms.local

Instructor B:
teacher2@test.progressrooms.local
```

---

## Students

```text
student1@test.progressrooms.local

student2@test.progressrooms.local

student3@test.progressrooms.local
```

Do not store production credentials.

These are development/test accounts only.

---

# 112. TEST DATABASE SEED SYSTEM

Create a dedicated test seed system.

Folder:

```text
/scripts/seed
```

or:

```text
/tests/seed-data
```

The seed script should create realistic data.

---

# 113. REQUIRED SEED DATA

Create:

## Platform

```text
One Super Admin
```

---

## Organization A

```text
Sahil Yoga Studio
```

Data:

```text
Owner

2 Instructors

20 Students

Yoga Class Type

Aerial Yoga Class Type

Multiple Sessions

Upcoming Classes

Completed Classes

Cancelled Class

Rescheduled Class
```

---

## Organization B

```text
John Guitar Academy
```

Data:

```text
Owner

3 Instructors

15 Students

Guitar Class Type

Beginner Guitar

Advanced Guitar

Private Guitar Session
```

---

## Organization C

```text
Dance Studio
```

Use a different plan.

---

# 114. REQUIRED PAYMENT TEST DATA

Seed:

```text
Successful Order

Failed Payment

Pending Payment

Expired Enrollment

Active Enrollment

Class Package Enrollment
```

Use mock payment records for development.

---

# 115. REQUIRED WEBSITE TEST DATA

Seed:

```text
Default Website Organization

Studio Plan Organization

Template A Website

Template B Website

Template C Website
```

Include:

```text
Images

Descriptions

Sessions

Contact Details
```

---

# 116. DATABASE SEED SCRIPT REQUIREMENTS

The seed process should be:

```text
Repeatable

Idempotent where practical

Documented

Environment aware
```

Provide commands:

```text
Reset Database

Run Migrations

Seed Test Data

Run Tests
```

---

# 117. TESTING REQUIREMENTS

Implement:

## Unit Tests

For:

```text
Plan Entitlements

Pricing Calculation

Enrollment Logic

Schedule Generation

Class Consumption

Authorization
```

---

## Integration Tests

For:

```text
Database Operations

Payment Webhooks

Enrollment Flow

Zoom Integration Mock

Notification Jobs
```

---

## End-to-End Tests

For:

```text
Teacher Signup

Plan Selection

Session Creation

Public Website

Student Discovery

OTP Login

Payment

Enrollment

Student Dashboard
```

---

# 118. CRITICAL END-TO-END TEST SCENARIO

Implement and document this complete scenario:

```text
Teacher Creates Account
        ↓
Teacher Gets Trial
        ↓
Teacher Creates Organization
        ↓
Teacher Creates Class Type
        ↓
Teacher Creates Session
        ↓
Teacher Adds Pricing
        ↓
Teacher Adds Schedule
        ↓
Class Occurrences Generated
        ↓
Public Website Shows Session
        ↓
Visitor Opens Website
        ↓
Visitor Opens Session
        ↓
Visitor Clicks Enroll
        ↓
Visitor Logs In With Email OTP
        ↓
Order Created
        ↓
Razorpay Checkout
        ↓
Webhook Confirms Payment
        ↓
Enrollment Activated
        ↓
Student Dashboard Updated
        ↓
Upcoming Classes Visible
        ↓
Student Joins Zoom Class
        ↓
Teacher Marks Attendance
        ↓
Enrollment Usage Updated
        ↓
Expiry Reminder Sent
```

This flow must work end-to-end.

---

# 119. DEVELOPMENT ENVIRONMENT

Maintain:

```text
Development

Testing

Staging

Production
```

Environment variables must be documented.

Example:

```text
DATABASE_URL

RAZORPAY_KEY_ID

RAZORPAY_KEY_SECRET

ZOOM_CLIENT_ID

ZOOM_CLIENT_SECRET

EMAIL_PROVIDER_KEY

STORAGE_PROVIDER_KEY
```

Never commit secrets.

---

# 120. DATABASE MIGRATION STRATEGY

All database changes must use migrations.

Never manually modify production database schema.

Workflow:

```text
Schema Change
        ↓
Migration Created
        ↓
Migration Tested
        ↓
Applied to Development
        ↓
Applied to Staging
        ↓
Applied to Production
```

---

# 121. SECURITY REQUIREMENTS

Implement:

```text
Secure Authentication

OTP Expiration

OTP Rate Limiting

Password Hashing if passwords are added

Token Security

Role Authorization

Organization Isolation

Input Validation

Rate Limiting

Webhook Signature Validation

Credential Encryption

Secure Headers

Audit Logging
```

---

# 122. DATA PRIVACY

Ensure:

```text
Students cannot access other students' information.

Teachers cannot access another organization's data.

Public users cannot access private sessions.

Meeting URLs are protected.

Payment information is not exposed.
```

---

# 123. FUTURE AI PLAN PREPARATION

Do not implement AI features now.

However, preserve the plan:

```text
Progress AI
```

Potential future modules:

```text
AI Assistant

AI Website Content

AI Class Description Generator

AI Student Insights

AI Marketing Generator

AI Scheduling Suggestions
```

Feature entitlements should allow future activation.

---

# 124. MVP PRIORITIES

## Phase 1

Foundation:

```text
Authentication

Organizations

Roles

Plans

Subscriptions

Database Architecture
```

---

## Phase 2

Core Teacher Features:

```text
Class Types

Sessions

Teachers

Students

Scheduling

Calendar
```

---

## Phase 3

Public Platform:

```text
Public Teacher Pages

SSR

Session Pages

SEO
```

---

## Phase 4

Commerce:

```text
Pricing

Orders

Razorpay

Payments

Enrollments
```

---

## Phase 5

Student Experience:

```text
Student Dashboard

Upcoming Classes

My Sessions

Enrollment Status

Join Classes
```

---

## Phase 6

Advanced Website:

```text
Template System

Template Selection

Content Management

Preview

Publishing
```

---

## Phase 7

Automation:

```text
Email Reminders

Enrollment Expiry

Class Reminders

Background Jobs
```

---

# 125. FINAL REQUIRED DEVELOPMENT WORKFLOW

The coding agent must NOT immediately begin implementing the entire application.

The following steps are mandatory.

---

## STEP 1 — DOMAIN ANALYSIS

Analyze the complete business domain.

Document:

```text
Users

Organizations

Sessions

Students

Payments

Enrollments

Plans

Websites

Scheduling
```

Store documentation:

```text
/docs/01-product/domain-model.md
```

---

## STEP 2 — ENTITY RELATIONSHIP DIAGRAM

Create a complete ER diagram.

Include every major entity.

Include:

```text
Primary Keys

Foreign Keys

Relationships

Cardinality
```

Store:

```text
/docs/03-database/er-diagram.md
```

Do not proceed until the ER model is internally consistent.

---

## STEP 3 — COMPLETE POSTGRESQL SCHEMA

Design every table.

For every table document:

```text
Column Name

Data Type

Nullable

Default

Primary Key

Foreign Key

Indexes

Constraints

Purpose
```

Store:

```text
/docs/03-database/schema.md
```

---

## STEP 4 — DATABASE MIGRATIONS

Create actual PostgreSQL migrations.

Store migrations in the project's database migration folder.

Document migration strategy.

---

## STEP 5 — ROLE AND AUTHORIZATION MATRIX

Create a complete matrix.

Example:

| Action | Super Admin | Owner | Admin | Instructor | Student |
| ------ | ----------- | ----- | ----- | ---------- | ------- |

Include every major operation.

Store:

```text
/docs/05-auth/authorization-matrix.md
```

---

## STEP 6 — USER FLOWS

Document detailed flows for:

```text
Teacher Signup

Teacher Trial

Plan Upgrade

Teacher Session Creation

Teacher Scheduling

Teacher Website Setup

Student Discovery

Student Login

Student Payment

Student Enrollment

Class Attendance

Enrollment Renewal
```

Store:

```text
/docs/04-user-flows/
```

---

## STEP 7 — API DESIGN

Define API contracts before implementation.

Document:

```text
Endpoint

Method

Authentication

Authorization

Request

Response

Errors
```

Store:

```text
/docs/04-api/api-specification.md
```

---

## STEP 8 — SCHEDULING ENGINE DESIGN

Before implementation, document:

```text
Recurrence Rules

Occurrence Generation

Cancellation

Rescheduling

Timezone Handling

Conflict Detection
```

Store:

```text
/docs/07-scheduling/scheduling-engine.md
```

---

## STEP 9 — PAYMENT DESIGN

Document:

```text
Order Creation

Payment Initiation

Razorpay Checkout

Webhook Processing

Payment Verification

Refunds

Enrollment Activation
```

Store:

```text
/docs/06-payments/payment-architecture.md
```

---

## STEP 10 — SUBSCRIPTION AND PLAN DESIGN

Document:

```text
Trial

Starter

Core

Studio

Progress AI

Feature Entitlements

Usage Limits

Plan Changes
```

Store:

```text
/docs/01-product/subscription-plans.md
```

---

## STEP 11 — WEBSITE SYSTEM DESIGN

Document:

```text
Public Routing

SSR

Templates

Content Configuration

Session Integration

SEO

Media
```

Store:

```text
/docs/08-websites/website-system.md
```

---

## STEP 12 — TEST DATA DESIGN

Create realistic test organizations.

Create:

```text
Super Admin

Multiple Teachers

Multi-Teacher Studio

Students

Sessions

Schedules

Payments

Enrollments
```

Document:

```text
/docs/09-testing/test-data.md
```

---

## STEP 13 — TEST DATABASE SCRIPT

Create scripts capable of:

```text
Resetting Development Database

Running Migrations

Creating Test Data
```

Store:

```text
/scripts/seed/
```

Document usage.

---

## STEP 14 — IMPLEMENT CORE FOUNDATION

Only after all architecture documentation is complete:

Implement:

```text
Database

Authentication

Organizations

Authorization

Plans

Subscriptions
```

---

## STEP 15 — IMPLEMENT CLASS MANAGEMENT

Implement:

```text
Class Types

Sessions

Teachers

Students

Session Assignment
```

---

## STEP 16 — IMPLEMENT SCHEDULING

Implement:

```text
Schedule Rules

Class Occurrences

Calendar

Rescheduling

Cancellation
```

---

## STEP 17 — IMPLEMENT PUBLIC SSR WEBSITE

Implement:

```text
Organization Public Page

Session Listing

Session Detail

SEO Metadata
```

---

## STEP 18 — IMPLEMENT STUDENT COMMERCE

Implement:

```text
Authentication

Session Purchase

Order Creation

Razorpay

Webhook

Enrollment
```

---

## STEP 19 — IMPLEMENT STUDENT DASHBOARD

Implement:

```text
Upcoming Classes

My Sessions

Enrollment Details

Payments

Join Class
```

---

## STEP 20 — IMPLEMENT ADVANCED WEBSITE

Implement:

```text
Template System

3 Templates

Customization

Preview

Publish
```

---

## STEP 21 — IMPLEMENT BACKGROUND JOBS

Implement:

```text
Class Generation

Email Notifications

Class Reminders

Enrollment Expiry Checks
```

---

## STEP 22 — COMPLETE TESTING

Run:

```text
Unit Tests

Integration Tests

End-to-End Tests

Payment Tests

Authorization Tests

Multi-Tenant Isolation Tests
```

---

## STEP 23 — DOCUMENT EVERYTHING

Every completed feature must update relevant documentation.

No undocumented major architecture changes.

---

# FINAL ENGINEERING PRINCIPLES

The application must prioritize:

```text
Correct Architecture

Multi-Tenant Isolation

Data Integrity

Security

Extensibility

Clean User Experience
```

over:

```text
Quick CRUD Development

Hardcoded Plan Logic

Duplicate Data

Frontend-Only Authorization

Business Logic Mixed With UI
```

The application should scale from:

```text
One Independent Teacher
```

to:

```text
Thousands of Organizations

Tens of Thousands of Teachers

Hundreds of Thousands of Students

Millions of Class Occurrences
```

without requiring a fundamental architectural rewrite.

---

# FINAL INSTRUCTION TO CODING AGENT

Do not blindly implement features.

Before every major module:

```text
Understand Domain
        ↓
Document Design
        ↓
Validate Relationships
        ↓
Define API
        ↓
Write Tests
        ↓
Implement
        ↓
Test
        ↓
Update Documentation
```

The `/docs` folder is part of the product deliverable.

The `/tests` folder is part of the product deliverable.

The database seed system is part of the product deliverable.

No major feature should be considered complete without:

```text
Architecture Documentation

Database Validation

Authorization Validation

Automated Tests

Relevant Seed Data

End-to-End Scenario Coverage
```
