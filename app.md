## Hawk Event

### Story

* The application is a comprehensive system for creating, organizing, and managing events. Each event includes:

    * Attributes: Unique identifier, name, description, start date, end date, slug, and status.
    * Location Information (optional): local, neighborhood, city, state, and zip code.
    * Organizer: Each event is managed by a designated organizer.

* Users of the system can either organize events or register as participants in other events. Each user has specific access permissions and is defined by:

    * Attributes: Unique identifier, name, email, and password.
    * Event Registrations: A user can register for multiple events, and each event can have multiple registrants.

* Activities form the core of an event's schedule. They include:

    * Attributes: Unique identifier, name, description, date, start time, end time, price, and status.
    * Association with Speakers: Each activity is linked to a speaker who will present it.

* Lots (Ticket Sales) - Events may have multiple lots for ticket sales, each with specific attributes:

    * Attributes: Unique identifier, name, description, quantity, price, start date, end date, and status (active or inactive).
    * Event Association: Each lot is linked to a specific event.
    * Functionality:
        * Lots are used to manage ticket availability and pricing tiers (e.g., Early Bird, Regular, Last Minute).
        * Users can purchase tickets from available lots until the defined quantity is sold out or the end date is reached.
        * The system tracks ticket availability to prevent overselling.

* Purchase - Register a purchase made by a user for an event, linked to a specific lot.
    * Attributes: id, user_id, lot_id, amount, status, payment_method
    * Status: can be pending, completed, failed, canceled.
    * Association: related to User, Event and Lot.

* Payment - Register payment details related to a Purchase.
    * Attributes: id, purchase_id, transaction_id, amount, payment_method, status, payment_date
    * Status: can be successful, failed, refunded.
    * Association: relates to Purchase.

* Invoice - Represents an invoice generated after a purchase.
    * Attributes: id, purchase_id, user_id, event_id, total_amount, issue_date, due_date, status
    * Status: can be unpaid, paid, overdue.
    * Association: related to Purchase and User.

This system aims to streamline event management, ensuring smooth coordination between organizers, participants, and speakers.

### Logic

- User (id, username, email, password, role_id)
- Event (id, name, description, date_start, date_end, slug, status, organizer_id)
- EventAddress (id, local, neighborhood, city, state, zip_code, event_id)
- EventUser (id, event_id, user_id)
- Activity (id, name, description, date, start_time, end_time, price, status, speaker_id, event_id)
- Lot (id, name, description, quantity, price, date_start, date_end, active, event_id)
- Purchase (id, user_id, lot_id, amount, status, payment_method)
- Payment (id, purchase_id, transaction_id, amount, payment_method, status, payment_date)
- Invoice (id, purchase_id, user_id, event_id, total_amount, issue_date, due_date, status)
- Wallet (id, user_id, event_id, payment_method enum('bill','card', 'pix'), token, secret, access_token, public_key, private_key, auth_key, refresh_token, expired_in)