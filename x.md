Supported Tokens
================

Use the following tokens in parsing and formatting. Note that they're
not the same as the tokens for
[strptime(3)](https://www.gnu.org/software/libc/manual/html_node/Low_002dLevel-Time-String-Parsing.html#index-strptime):

  ------------------------------------------------------------------------
                            Token       Output
  ------------------------- ----------- ----------------------------------
  **Year**                  YYYY        2000, 2001, 2002 ... 2012, 2013

                            YY          00, 01, 02 ... 12, 13

  **Month**                 MMMM        January, February, March ... [^1]

                            MMM         Jan, Feb, Mar ... [^2]

                            MM          01, 02, 03 ... 11, 12

                            M           1, 2, 3 ... 11, 12

  **Day of Year**           DDDD        001, 002, 003 ... 364, 365

                            DDD         1, 2, 3 ... 364, 365

  **Day of Month**          DD          01, 02, 03 ... 30, 31

                            D           1, 2, 3 ... 30, 31

                            Do          1st, 2nd, 3rd ... 30th, 31st

  **Day of Week**           dddd        Monday, Tuesday, Wednesday ...
                                        [^3]

                            ddd         Mon, Tue, Wed ... [^4]

                            d           1, 2, 3 ... 6, 7

  **Hour**                  HH          00, 01, 02 ... 23, 24

                            H           0, 1, 2 ... 23, 24

                            hh          01, 02, 03 ... 11, 12

                            h           1, 2, 3 ... 11, 12

  **AM / PM**               A           AM, PM, am, pm [^5]

                            a           am, pm [^6]

  **Minute**                mm          00, 01, 02 ... 58, 59

                            m           0, 1, 2 ... 58, 59

  **Second**                ss          00, 01, 02 ... 58, 59

                            s           0, 1, 2 ... 58, 59

  **Sub-second**            S...        0, 02, 003, 000006,
                                        123123123123... [^7]

  **Timezone**              ZZZ         Asia/Baku, Europe/Warsaw, GMT ...
                                        [^8]

                            ZZ          -07:00, -06:00 ... +06:00, +07:00,
                                        +08, Z

                            Z           -0700, -0600 ... +0600, +0700,
                                        +08, Z

  **Seconds Timestamp**     X           1381685817, 1381685817.915482 ...
                                        [^9]

  **ms or µs Timestamp**    x           1569980330813, 1569980330813221
  ------------------------------------------------------------------------

**Footnotes**

[^1]: localization support for parsing and formatting

[^2]: localization support for parsing and formatting

[^3]: localization support only for formatting

[^4]: localization support only for formatting

[^5]: localization support for parsing and formatting

[^6]: localization support for parsing and formatting

[^7]: the result is truncated to microseconds, with [half-to-even
    rounding](https://en.wikipedia.org/wiki/IEEE_floating_point#Roundings_to_nearest).

[^8]: timezone names from [tz database](https://www.iana.org/time-zones)
    provided via dateutil package

[^9]: this token cannot be used for parsing timestamps out of natural
    language strings due to compatibility reasons
