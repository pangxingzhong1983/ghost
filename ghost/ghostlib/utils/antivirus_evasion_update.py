#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2026, Ghost Project

# Ghost is under the BSD 3-Clause license. see the LICENSE file at the
# root of the project for the detailed licence terms

import os
import sys
import time
import threading
import datetime

from ghost.ghostlib.GhostConfig import GhostConfig
from ghost.ghostlib.utils.antivirus_evasion import AntivirusEvasion
from ghost.ghostlib.GhostLogger import getLogger

logger = getLogger('antivirus_evasion_update')

class AntivirusEvasionUpdater:
    def __init__(self, config=None):
        self.config = config or GhostConfig()
        self.av_evasion = AntivirusEvasion(self.config)
        self.update_interval = 24  # hours
        self.running = False
        self.thread = None
    
    def start(self):
        """Start the antivirus evasion updater"""
        if self.running:
            logger.info('Antivirus evasion updater is already running')
            return
        
        self.running = True
        # Run the first update immediately
        self.update_evasion_techniques()
        
        # Start the update loop in a separate thread
        self.thread = threading.Thread(target=self._update_loop)
        self.thread.daemon = True
        self.thread.start()
        
        logger.info(f'Antivirus evasion updater started with {self.update_interval} hour interval')
    
    def stop(self):
        """Stop the antivirus evasion updater"""
        if not self.running:
            logger.info('Antivirus evasion updater is not running')
            return
        
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        
        logger.info('Antivirus evasion updater stopped')
    
    def _update_loop(self):
        """Run the update loop"""
        while self.running:
            # Wait for the update interval
            for _ in range(self.update_interval * 60):  # Convert hours to minutes
                if not self.running:
                    break
                time.sleep(60)  # Sleep for 1 minute
            
            if self.running:
                self.update_evasion_techniques()
    
    def update_evasion_techniques(self):
        """Update evasion techniques"""
        try:
            logger.info('Updating antivirus evasion techniques...')
            self.av_evasion.check_for_updates()
            status = self.av_evasion.get_evasion_status()
            logger.info(f'Evasion techniques updated successfully: {status}')
            
            # Generate evasion report
            report = self.av_evasion.generate_evasion_report()
            logger.info(f'Evasion report generated: {report["timestamp"]}')
        except Exception as e:
            logger.error(f'Error updating evasion techniques: {e}')
    
    def get_status(self):
        """Get the status of the updater"""
        return {
            'running': self.running,
            'update_interval': self.update_interval,
            'last_update': self.av_evasion.last_update_check.isoformat() if self.av_evasion.last_update_check else None,
            'evasion_status': self.av_evasion.get_evasion_status()
        }

if __name__ == '__main__':
    # Test the updater
    updater = AntivirusEvasionUpdater()
    updater.start()
    
    try:
        # Run for 10 minutes
        for i in range(10):
            print(f'\nStatus at {datetime.datetime.now()}:')
            print(updater.get_status())
            time.sleep(60)
    finally:
        updater.stop()