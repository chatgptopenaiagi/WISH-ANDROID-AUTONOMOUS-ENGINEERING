# Graphical Hub port — design stage

The Vivo Hub is verified reference software; its private installation is not copied
here. A portable interface must retain wish input, genuine status/events, project
discovery, capability search, resource views, fixed application registrations and
contained artifact delivery. Romanian and English input must remain simple.

The proposed backend contract separates session availability, queued receipt,
running confirmation and verified completion. Use SSE or an equivalent bounded
event stream; never fabricate progress. The runtime owner authenticates requests.

The initial product can open a verified loopback URL in a browser. Embedded WebView
integration is a later decision after origin, navigation, export, XSS and bridge
tests. There is no production Hub backend or Android JavaScript bridge in M1.
