# LockBox_Destruction
My personal sandbox for experimenting with and reproducing distributed backend bugs under real-world conditions.

---

## What This Is

Before building defenses, I am using this repo to write intentionally vulnerable backend code to observe how and why systems break under pressure. 

Each scenario, hits it with concurrent traffic or forced crashes, and exposes the failure directly in the terminal.

---

##

### The Race Condition (Free Money Glitch)
* **Setup:** An account initialized with **$100**.
* **Test:** Firing 10 simultaneous requests at the exact same millisecond to withdraw **$100**.
* **Expected Result:** 1 success, 9 rejections, balance at **$0**.
* **Observed Failure:** Multiple requests read the old `$100` balance before any update writes. Multiple withdrawals succeed, dispensing $300–$1,000 from a $100 deposit while returning 200 OK.

---

### The Double-Click Trap (Network Replay)
* **Setup:** A checkout endpoint with an artificial 2-second processing delay.
* **Test:** Simulating an impatient user clicking "Pay $50" three times within 500 milliseconds.
* **Expected Result:** 1 charge of $50, 1 receipt.
* **Observed Failure:** 3 parallel routines run. The account gets billed **$150**, creating 3 separate charges for 1 item.

---

### The Ghost Order (Dual-Write Failure)
* **Setup:** An endpoint that updates the database, then sends an event to an external service.
* **Test:** Injecting a process crash (`SIGKILL`) immediately after the database write finishes, before the network event fires.
* **Expected Result:** State stays consistent across both systems.
* **Observed Failure:** The money is deducted from the database, but the event never sends. The user is charged, the goods never ship, and the system loses track of the transaction.
