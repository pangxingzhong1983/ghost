# -*- coding: utf-8 -*-
# --------------------------------------------------------------
# Copyright (c) 2015, Nicolas VERDIER (contact@n1nj4.eu)
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided
# that the following conditions are met:
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and
# the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and
# the following disclaimer in the documentation and/or other materials provided with the distribution.
# 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or
# promote products derived from this software without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE
# --------------------------------------------------------------

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from ghost.ghostlib.GhostModule import config, GhostModule, GhostArgumentParser

__class_name__ = "Browser"


@config(cat="gather", compat=['windows', 'linux', 'darwin'])
class Browser(GhostModule):
    """ Browser history, bookmarks and credentials extraction """

    dependencies = {
        'windows': [],
        'linux': [],
        'darwin': []
    }

    @classmethod
    def init_argparse(cls):
        cls.arg_parser = GhostArgumentParser(prog="browser", description=cls.__doc__)
        cls.arg_parser.add_argument(
            '-t', '--type', choices=['history', 'bookmarks', 'credentials', 'cookies', 'all'],
            default='all', help='Type of data to extract')
        cls.arg_parser.add_argument(
            '-b', '--browser', choices=['chrome', 'firefox', 'edge', 'safari', 'all'],
            default='all', help='Browser to extract data from')
        cls.arg_parser.add_argument(
            '-o', '--output', help='Output file path')

    def run(self, args):
        if self.client.is_windows():
            self.windows(args)
        elif self.client.is_linux():
            self.linux(args)
        elif self.client.is_darwin():
            self.darwin(args)
        else:
            self.error('Browser module not supported on this platform')

    def windows(self, args):
        """ Extract browser data on Windows """
        self.info('Extracting browser data on Windows')
        
        browsers = []
        if args.browser == 'all' or args.browser == 'chrome':
            browsers.append('chrome')
        if args.browser == 'all' or args.browser == 'firefox':
            browsers.append('firefox')
        if args.browser == 'all' or args.browser == 'edge':
            browsers.append('edge')
        
        for browser in browsers:
            self.info(f'Processing {browser}')
            
            if args.type == 'all' or args.type == 'history':
                self._extract_history_windows(browser)
            if args.type == 'all' or args.type == 'bookmarks':
                self._extract_bookmarks_windows(browser)
            if args.type == 'all' or args.type == 'credentials':
                self._extract_credentials_windows(browser)
            if args.type == 'all' or args.type == 'cookies':
                self._extract_cookies_windows(browser)

    def linux(self, args):
        """ Extract browser data on Linux """
        self.info('Extracting browser data on Linux')
        
        browsers = []
        if args.browser == 'all' or args.browser == 'chrome':
            browsers.append('chrome')
        if args.browser == 'all' or args.browser == 'firefox':
            browsers.append('firefox')
        
        for browser in browsers:
            self.info(f'Processing {browser}')
            
            if args.type == 'all' or args.type == 'history':
                self._extract_history_linux(browser)
            if args.type == 'all' or args.type == 'bookmarks':
                self._extract_bookmarks_linux(browser)
            if args.type == 'all' or args.type == 'credentials':
                self._extract_credentials_linux(browser)
            if args.type == 'all' or args.type == 'cookies':
                self._extract_cookies_linux(browser)

    def darwin(self, args):
        """ Extract browser data on MacOS """
        self.info('Extracting browser data on MacOS')
        
        browsers = []
        if args.browser == 'all' or args.browser == 'chrome':
            browsers.append('chrome')
        if args.browser == 'all' or args.browser == 'firefox':
            browsers.append('firefox')
        if args.browser == 'all' or args.browser == 'safari':
            browsers.append('safari')
        
        for browser in browsers:
            self.info(f'Processing {browser}')
            
            if args.type == 'all' or args.type == 'history':
                self._extract_history_darwin(browser)
            if args.type == 'all' or args.type == 'bookmarks':
                self._extract_bookmarks_darwin(browser)
            if args.type == 'all' or args.type == 'credentials':
                self._extract_credentials_darwin(browser)
            if args.type == 'all' or args.type == 'cookies':
                self._extract_cookies_darwin(browser)

    def _extract_history_windows(self, browser):
        """ Extract browser history on Windows """
        try:
            if browser == 'chrome':
                # Chrome history path on Windows
                history_path = r'%LOCALAPPDATA%\Google\Chrome\User Data\Default\History'
                self.success(f'Chrome history path: {history_path}')
                # TODO: Implement actual extraction
            elif browser == 'firefox':
                # Firefox history path on Windows
                history_path = r'%APPDATA%\Mozilla\Firefox\Profiles\*.default\places.sqlite'
                self.success(f'Firefox history path: {history_path}')
                # TODO: Implement actual extraction
            elif browser == 'edge':
                # Edge history path on Windows
                history_path = r'%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\History'
                self.success(f'Edge history path: {history_path}')
                # TODO: Implement actual extraction
        except Exception as e:
            self.error(f'Error extracting {browser} history: {e}')

    def _extract_bookmarks_windows(self, browser):
        """ Extract browser bookmarks on Windows """
        try:
            if browser == 'chrome':
                # Chrome bookmarks path on Windows
                bookmarks_path = r'%LOCALAPPDATA%\Google\Chrome\User Data\Default\Bookmarks'
                self.success(f'Chrome bookmarks path: {bookmarks_path}')
                # TODO: Implement actual extraction
            elif browser == 'firefox':
                # Firefox bookmarks path on Windows
                bookmarks_path = r'%APPDATA%\Mozilla\Firefox\Profiles\*.default\places.sqlite'
                self.success(f'Firefox bookmarks path: {bookmarks_path}')
                # TODO: Implement actual extraction
            elif browser == 'edge':
                # Edge bookmarks path on Windows
                bookmarks_path = r'%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\Bookmarks'
                self.success(f'Edge bookmarks path: {bookmarks_path}')
                # TODO: Implement actual extraction
        except Exception as e:
            self.error(f'Error extracting {browser} bookmarks: {e}')

    def _extract_credentials_windows(self, browser):
        """ Extract browser credentials on Windows """
        try:
            if browser == 'chrome':
                # Chrome credentials path on Windows
                login_data_path = r'%LOCALAPPDATA%\Google\Chrome\User Data\Default\Login Data'
                self.success(f'Chrome credentials path: {login_data_path}')
                # TODO: Implement actual extraction
            elif browser == 'firefox':
                # Firefox credentials path on Windows
                logins_json_path = r'%APPDATA%\Mozilla\Firefox\Profiles\*.default\logins.json'
                self.success(f'Firefox credentials path: {logins_json_path}')
                # TODO: Implement actual extraction
            elif browser == 'edge':
                # Edge credentials path on Windows
                login_data_path = r'%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\Login Data'
                self.success(f'Edge credentials path: {login_data_path}')
                # TODO: Implement actual extraction
        except Exception as e:
            self.error(f'Error extracting {browser} credentials: {e}')

    def _extract_cookies_windows(self, browser):
        """ Extract browser cookies on Windows """
        try:
            if browser == 'chrome':
                # Chrome cookies path on Windows
                cookies_path = r'%LOCALAPPDATA%\Google\Chrome\User Data\Default\Cookies'
                self.success(f'Chrome cookies path: {cookies_path}')
                # TODO: Implement actual extraction
            elif browser == 'firefox':
                # Firefox cookies path on Windows
                cookies_path = r'%APPDATA%\Mozilla\Firefox\Profiles\*.default\cookies.sqlite'
                self.success(f'Firefox cookies path: {cookies_path}')
                # TODO: Implement actual extraction
            elif browser == 'edge':
                # Edge cookies path on Windows
                cookies_path = r'%LOCALAPPDATA%\Microsoft\Edge\User Data\Default\Cookies'
                self.success(f'Edge cookies path: {cookies_path}')
                # TODO: Implement actual extraction
        except Exception as e:
            self.error(f'Error extracting {browser} cookies: {e}')

    def _extract_history_linux(self, browser):
        """ Extract browser history on Linux """
        try:
            if browser == 'chrome':
                # Chrome history path on Linux
                history_path = '~/.config/google-chrome/Default/History'
                self.success(f'Chrome history path: {history_path}')
                # TODO: Implement actual extraction
            elif browser == 'firefox':
                # Firefox history path on Linux
                history_path = '~/.mozilla/firefox/*.default/places.sqlite'
                self.success(f'Firefox history path: {history_path}')
                # TODO: Implement actual extraction
        except Exception as e:
            self.error(f'Error extracting {browser} history: {e}')

    def _extract_bookmarks_linux(self, browser):
        """ Extract browser bookmarks on Linux """
        try:
            if browser == 'chrome':
                # Chrome bookmarks path on Linux
                bookmarks_path = '~/.config/google-chrome/Default/Bookmarks'
                self.success(f'Chrome bookmarks path: {bookmarks_path}')
                # TODO: Implement actual extraction
            elif browser == 'firefox':
                # Firefox bookmarks path on Linux
                bookmarks_path = '~/.mozilla/firefox/*.default/places.sqlite'
                self.success(f'Firefox bookmarks path: {bookmarks_path}')
                # TODO: Implement actual extraction
        except Exception as e:
            self.error(f'Error extracting {browser} bookmarks: {e}')

    def _extract_credentials_linux(self, browser):
        """ Extract browser credentials on Linux """
        try:
            if browser == 'chrome':
                # Chrome credentials path on Linux
                login_data_path = '~/.config/google-chrome/Default/Login Data'
                self.success(f'Chrome credentials path: {login_data_path}')
                # TODO: Implement actual extraction
            elif browser == 'firefox':
                # Firefox credentials path on Linux
                logins_json_path = '~/.mozilla/firefox/*.default/logins.json'
                self.success(f'Firefox credentials path: {logins_json_path}')
                # TODO: Implement actual extraction
        except Exception as e:
            self.error(f'Error extracting {browser} credentials: {e}')

    def _extract_cookies_linux(self, browser):
        """ Extract browser cookies on Linux """
        try:
            if browser == 'chrome':
                # Chrome cookies path on Linux
                cookies_path = '~/.config/google-chrome/Default/Cookies'
                self.success(f'Chrome cookies path: {cookies_path}')
                # TODO: Implement actual extraction
            elif browser == 'firefox':
                # Firefox cookies path on Linux
                cookies_path = '~/.mozilla/firefox/*.default/cookies.sqlite'
                self.success(f'Firefox cookies path: {cookies_path}')
                # TODO: Implement actual extraction
        except Exception as e:
            self.error(f'Error extracting {browser} cookies: {e}')

    def _extract_history_darwin(self, browser):
        """ Extract browser history on MacOS """
        try:
            if browser == 'chrome':
                # Chrome history path on MacOS
                history_path = '~/Library/Application Support/Google/Chrome/Default/History'
                self.success(f'Chrome history path: {history_path}')
                # TODO: Implement actual extraction
            elif browser == 'firefox':
                # Firefox history path on MacOS
                history_path = '~/Library/Application Support/Firefox/Profiles/*.default/places.sqlite'
                self.success(f'Firefox history path: {history_path}')
                # TODO: Implement actual extraction
            elif browser == 'safari':
                # Safari history path on MacOS
                history_path = '~/Library/Safari/History.db'
                self.success(f'Safari history path: {history_path}')
                # TODO: Implement actual extraction
        except Exception as e:
            self.error(f'Error extracting {browser} history: {e}')

    def _extract_bookmarks_darwin(self, browser):
        """ Extract browser bookmarks on MacOS """
        try:
            if browser == 'chrome':
                # Chrome bookmarks path on MacOS
                bookmarks_path = '~/Library/Application Support/Google/Chrome/Default/Bookmarks'
                self.success(f'Chrome bookmarks path: {bookmarks_path}')
                # TODO: Implement actual extraction
            elif browser == 'firefox':
                # Firefox bookmarks path on MacOS
                bookmarks_path = '~/Library/Application Support/Firefox/Profiles/*.default/places.sqlite'
                self.success(f'Firefox bookmarks path: {bookmarks_path}')
                # TODO: Implement actual extraction
            elif browser == 'safari':
                # Safari bookmarks path on MacOS
                bookmarks_path = '~/Library/Safari/Bookmarks.plist'
                self.success(f'Safari bookmarks path: {bookmarks_path}')
                # TODO: Implement actual extraction
        except Exception as e:
            self.error(f'Error extracting {browser} bookmarks: {e}')

    def _extract_credentials_darwin(self, browser):
        """ Extract browser credentials on MacOS """
        try:
            if browser == 'chrome':
                # Chrome credentials path on MacOS
                login_data_path = '~/Library/Application Support/Google/Chrome/Default/Login Data'
                self.success(f'Chrome credentials path: {login_data_path}')
                # TODO: Implement actual extraction
            elif browser == 'firefox':
                # Firefox credentials path on MacOS
                logins_json_path = '~/Library/Application Support/Firefox/Profiles/*.default/logins.json'
                self.success(f'Firefox credentials path: {logins_json_path}')
                # TODO: Implement actual extraction
            elif browser == 'safari':
                # Safari credentials are stored in Keychain
                self.success('Safari credentials stored in Keychain')
                # TODO: Implement actual extraction
        except Exception as e:
            self.error(f'Error extracting {browser} credentials: {e}')

    def _extract_cookies_darwin(self, browser):
        """ Extract browser cookies on MacOS """
        try:
            if browser == 'chrome':
                # Chrome cookies path on MacOS
                cookies_path = '~/Library/Application Support/Google/Chrome/Default/Cookies'
                self.success(f'Chrome cookies path: {cookies_path}')
                # TODO: Implement actual extraction
            elif browser == 'firefox':
                # Firefox cookies path on MacOS
                cookies_path = '~/Library/Application Support/Firefox/Profiles/*.default/cookies.sqlite'
                self.success(f'Firefox cookies path: {cookies_path}')
                # TODO: Implement actual extraction
            elif browser == 'safari':
                # Safari cookies path on MacOS
                cookies_path = '~/Library/Cookies/Cookies.binarycookies'
                self.success(f'Safari cookies path: {cookies_path}')
                # TODO: Implement actual extraction
        except Exception as e:
            self.error(f'Error extracting {browser} cookies: {e}')