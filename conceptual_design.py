
   RUNNING           READY                 WAITING (on I/O)
    STATE            STATE                  STATE

   +-----+                               +-----------------+
   |     |     +--------------------+    |                 |
   | CPU | <== |    |    |    |     |    |  I/O Subsystem  |
   |     |     +--------------------+    |                 |
   +-----+      <<< queue <<<<<<<<<<     +-----------------+
