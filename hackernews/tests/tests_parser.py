from unittest import TestCase
from unittest.mock import MagicMock, patch
from urllib.error import HTTPError

from hackernews.parser import URL, HackerNewsParser

raw_text = """
<html op="news">
<head>
<meta name="referrer" content="origin"><meta name="viewport" content="width=device-width, initial-scale=1.0"><link rel="stylesheet" type="text/css" href="news.css?a6Wl6SU9GcO1K2QDIVYs">
            <link rel="shortcut icon" href="favicon.ico">
          <link rel="alternate" type="application/rss+xml" title="RSS" href="rss">
        <title>Hacker News</title>
        </head>
        <body>
        <center>
        <table id="hnmain" border="0" cellpadding="0" cellspacing="0" width="85%" bgcolor="#f6f6ef">
        <tr><td bgcolor="#ff6600"><table border="0" cellpadding="0" cellspacing="0" width="100%" style="padding:2px"><tr><td style="width:18px;padding-right:4px"><a href="https://news.ycombinator.com"><img src="y18.gif" width="18" height="18" style="border:1px white solid;"></a></td>
                  <td style="line-height:12pt; height:10px;"><span class="pagetop"><b class="hnname"><a href="news">Hacker News</a></b>
              <a href="newest">new</a> | <a href="front">past</a> | <a href="newcomments">comments</a> | <a href="ask">ask</a> | <a href="show">show</a> | <a href="jobs">jobs</a> | <a href="submit">submit</a>            </span></td><td style="text-align:right;padding-right:4px;"><span class="pagetop">
                              <a href="login?goto=news">login</a>
                          </span></td>
              </tr></table></td></tr>
<tr id="pagespace" title="" style="height:10px"></tr><tr><td><table border="0" cellpadding="0" cellspacing="0" class="itemlist">
              <tr class='athing' id='20719095'>
      <td align="right" valign="top" class="title"><span class="rank">1.</span></td>      <td valign="top" class="votelinks"><center><a id='up_20719095' href='vote?id=20719095&amp;how=up&amp;goto=news'><div class='votearrow' title='upvote'></div></a></center></td><td class="title"><a href="https://async.rs/blog/announcing-async-std/#" class="storylink">Async-std: an async port of the Rust standard library</a><span class="sitebit comhead"> (<a href="from?site=async.rs"><span class="sitestr">async.rs</span></a>)</span></td></tr><tr><td colspan="2"></td><td class="subtext">
        <span class="score" id="score_20719095">70 points</span> by <a href="user?id=JoshTriplett" class="hnuser">JoshTriplett</a> <span class="age"><a href="item?id=20719095">1 hour ago</a></span> <span id="unv_20719095"></span> | <a href="hide?id=20719095&amp;goto=news">hide</a> | <a href="item?id=20719095">21&nbsp;comments</a>              </td></tr>
      <tr class="spacer" style="height:5px"></tr>
                <tr class='athing' id='20715476'>
      <td align="right" valign="top" class="title"><span class="rank">2.</span></td>
      <td valign="top" class="votelinks"><center><a id='up_20715476' href='vote?id=20715476&amp;how=up&amp;goto=news'><div class='votearrow' title='upvote'></div></a></center></td>
      <td class="title"><a href="https://knobattack.com/" class="storylink">Key Negotiation of Bluetooth Attack</a><span class="sitebit comhead"> (<a href="from?site=knobattack.com"><span class="sitestr">knobattack.com</span></a>)</span></td>
      </tr><tr><td colspan="2"></td><td class="subtext">
        <span class="score" id="score_20715476">221 points</span> by <a href="user?id=Daviey" class="hnuser">Daviey</a> <span class="age"><a href="item?id=20715476">6 hours ago</a></span> <span id="unv_20715476"></span> | <a href="hide?id=20715476&amp;goto=news">hide</a> | <a href="item?id=20715476">80&nbsp;comments</a>              </td></tr>
      <tr class="spacer" style="height:5px"></tr>
                <tr class='athing' id='20715188'>
      <td align="right" valign="top" class="title"><span class="rank">29.</span></td>      <td valign="top" class="votelinks"><center><a id='up_20715188' href='vote?id=20715188&amp;how=up&amp;goto=news'><div class='votearrow' title='upvote'></div></a></center></td><td class="title"><a href="https://twitter.com/BenBajarin/status/1162048579654963200" class="storylink">US Gen Z and the iMessage Lock-In</a><span class="sitebit comhead"> (<a href="from?site=twitter.com"><span class="sitestr">twitter.com</span></a>)</span></td></tr><tr><td colspan="2"></td><td class="subtext">
        <span class="score" id="score_20715188">61 points</span> by <a href="user?id=seapunk" class="hnuser">seapunk</a> <span class="age"><a href="item?id=20715188">5 hours ago</a></span> <span id="unv_20715188"></span> | <a href="hide?id=20715188&amp;goto=news">hide</a> | <a href="item?id=20715188">115&nbsp;comments</a>              </td></tr>
      <tr class="spacer" style="height:5px"></tr>
                <tr class='athing' id='20717238'>
      <td align="right" valign="top" class="title"><span class="rank">30.</span></td>      <td></td><td class="title"><a href="https://jobs.lever.co/buildzoom" class="storylink" rel="nofollow">BuildZoom (YC W13) is hiring – Help us make remodeling cheaper</a><span class="sitebit comhead"> (<a href="from?site=lever.co"><span class="sitestr">lever.co</span></a>)</span></td></tr><tr><td colspan="2"></td><td class="subtext">
        <span class="age"><a href="item?id=20717238">3 hours ago</a></span> | <a href="hide?id=20717238&amp;goto=news">hide</a>      </td></tr>
      <tr class="spacer" style="height:5px"></tr>
            <tr class="morespace" style="height:10px"></tr><tr><td colspan="2"></td><td class="title"><a href="news?p=2" class="morelink" rel="next">More</a></td></tr>
  </table>
</td></tr>
<tr><td><img src="s.gif" height="10" width="0"><table width="100%" cellspacing="0" cellpadding="1"><tr><td bgcolor="#ff6600"></td></tr></table><br><center><span class="yclinks"><a href="newsguidelines.html">Guidelines</a>
        | <a href="newsfaq.html">FAQ</a>
        | <a href="mailto:hn@ycombinator.com">Support</a>
        | <a href="https://github.com/HackerNews/API">API</a>
        | <a href="security.html">Security</a>
        | <a href="lists">Lists</a>
        | <a href="bookmarklet.html" rel="nofollow">Bookmarklet</a>
        | <a href="http://www.ycombinator.com/legal/">Legal</a>
        | <a href="http://www.ycombinator.com/apply/">Apply to YC</a>
        | <a href="mailto:hn@ycombinator.com">Contact</a></span><br><br><form method="get" action="//hn.algolia.com/">Search:
          <input type="text" name="q" value="" size="17" autocorrect="off" spellcheck="false" autocapitalize="off" autocomplete="false"></form>
            </center></td></tr>
      </table></center></body><script type='text/javascript' src='hn.js?a6Wl6SU9GcO1K2QDIVYs'></script>
  </html>
"""


class HackerNewsParserTest(TestCase):
    def setUp(self):
        self.parser = HackerNewsParser()
        self.magic = MagicMock()

    @patch('hackernews.parser.urlopen')
    def test_success_download(self, mock):
        self.magic.read.return_value = raw_text.encode()
        mock.return_value = self.magic

        self.parser.download()

        self.assertEqual(self.parser._html, raw_text)

    @patch('hackernews.parser.urlopen')
    def test_fail_download(self, mock):
        status_code_items = [400, 404, 500]
        for status_code in status_code_items:
            with self.subTest(msg=status_code):
                mock.side_effect = HTTPError(URL, code=status_code, msg='', hdrs='', fp=mock)

                with self.assertRaises(HTTPError):
                    self.parser.download()

    @patch('hackernews.parser.urlopen')
    def test_convert_to_json(self, mock):
        self.magic.read.return_value = raw_text.encode()
        mock.return_value = self.magic

        self.parser.download()

        got = self.parser.as_json()

        self.assertEqual(len(got), 4)
        self.assertListEqual(
            got,
            [
                {'hacker_news_id': '20719095', 'url': 'https://async.rs/blog/announcing-async-std/#', 'title': 'Async-std: an async port of the Rust standard library'},
                {'hacker_news_id': '20715476', 'url': 'https://knobattack.com/', 'title': 'Key Negotiation of Bluetooth Attack'},
                {'hacker_news_id': '20715188', 'url': 'https://twitter.com/BenBajarin/status/1162048579654963200','title': 'US Gen Z and the iMessage Lock-In'},
                {'hacker_news_id': '20717238', 'url': 'https://jobs.lever.co/buildzoom','title': 'BuildZoom (YC W13) is hiring – Help us make remodeling cheaper'},
            ]
        )
