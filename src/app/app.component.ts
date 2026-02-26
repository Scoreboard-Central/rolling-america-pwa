import {Component, OnInit} from '@angular/core';
import {RouterOutlet} from '@angular/router';
import {FormsModule} from '@angular/forms';
import {CommonModule} from '@angular/common';

import {stateAdjacencies} from './map-data';

export interface GameHistoryItem {
  id: string;
  date: string;
  xsCount: number;
  won: boolean;
}

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [ RouterOutlet, FormsModule, CommonModule ],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent implements OnInit {
  title = 'rolling-america-pwa';

  // Modal State
  isModalOpen = false;
  isResetModalOpen = false;

  // New Modals
  isSettingsModalOpen = false;
  isHistoryModalOpen = false;
  isDeleteModalOpen = false;
  gameToDeleteId: string | null = null;
  
  get totalWins(): number {
    return this.gameHistory.filter(g => g.won).length;
  }
  
  get totalLosses(): number {
    return this.gameHistory.filter(g => !g.won).length;
  }

  // Theme & History
  isDarkMode = true;
  gameHistory: GameHistoryItem[] = [];

  // Intercept state
  gameWon = false;
  addToHistory = true;

  currentEditTarget: {type: 'state' | 'ability' | 'xs', key: string, index?: number} | null = null;
  validOptions: string[] = [ '1', '2', '3', '4', '5', '6' ];

  // Game State
  stateData: {[ key: string ]: string} = {};
  guardedStates: {[ key: string ]: boolean} = {};
  rounds: boolean[] = Array(8).fill(false);
  abilities = {
    colorChange: [ '', '', '' ],
    guard: [ '', '', '' ],
    dupe: [ '', '', '' ]
  };

  isGuardChecked = false;

  get guardsUsed(): number {
    return this.abilities.guard.filter(g => g === 'X').length;
  }

  get xsCount(): number {
    return Object.values(this.stateData).filter(v => v === 'X').length;
  }

  ngOnInit() {
    this.loadState();

    this.loadTheme();
    this.loadHistory();

  }

  saveState() {
    const saveData = {
      stateData: this.stateData,
      guardedStates: this.guardedStates,
      rounds: this.rounds,
      abilities: this.abilities
    };
    localStorage.setItem('rollingAmericaState', JSON.stringify(saveData));
  }

  loadState() {
    const saved = localStorage.getItem('rollingAmericaState');
    if (saved) {
      const parsed = JSON.parse(saved);
      this.stateData = parsed.stateData || {};
      this.guardedStates = parsed.guardedStates || {};
      this.rounds = parsed.rounds || Array(8).fill(false);
      this.abilities = parsed.abilities || {
        colorChange: [ '', '', '' ],
        guard: [ '', '', '' ],
        dupe: [ '', '', '' ]
      };
    }
  }


  loadTheme() {
    const savedTheme = localStorage.getItem('theme');
    // Default app to dark mode
    if (savedTheme === 'light') {
      this.isDarkMode = false;
    } else {
      this.isDarkMode = true;
      localStorage.setItem('theme', 'dark');
    }
    this.applyTheme();
  }

  toggleTheme() {
    this.isDarkMode = !this.isDarkMode;
    localStorage.setItem('theme', this.isDarkMode ? 'dark' : 'light');
    this.applyTheme();
  }

  applyTheme() {
    if (this.isDarkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }

  loadHistory() {
    const saved = localStorage.getItem('rollingAmericaHistory');
    if (saved) {
      try {
        this.gameHistory = JSON.parse(saved);
      } catch (e) {
        this.gameHistory = [];
      }
    }
  }

  saveHistory() {
    localStorage.setItem('rollingAmericaHistory', JSON.stringify(this.gameHistory));
  }

  deleteHistoryItem(id: string) {
    this.gameToDeleteId = id;
    this.isDeleteModalOpen = true;
  }

  cancelDelete() {
    this.isDeleteModalOpen = false;
    this.gameToDeleteId = null;
  }

  executeDelete() {
    if (this.gameToDeleteId) {
      this.gameHistory = this.gameHistory.filter(h => h.id !== this.gameToDeleteId);
      this.saveHistory();
    }
    this.cancelDelete();
  }

  openSettingsModal() {
    this.isSettingsModalOpen = true;
  }

  closeSettingsModal() {
    this.isSettingsModalOpen = false;
  }

  openHistoryModal() {
    this.isHistoryModalOpen = true;
  }

  closeHistoryModal() {
    this.isHistoryModalOpen = false;
  }


  openResetModal() {
    this.gameWon = false;
    this.addToHistory = true;
    this.isResetModalOpen = true;
  }

  closeResetModal() {
    this.isResetModalOpen = false;
  }

  confirmReset() {
    if (this.addToHistory) {
      const newItem: GameHistoryItem = {
        id: Date.now().toString() + Math.random().toString(36).substring(2, 9),
        date: new Date().toLocaleDateString(),
        xsCount: this.xsCount,
        won: this.gameWon
      };
      this.gameHistory.unshift(newItem);
      this.saveHistory();
    }

    this.stateData = {};
    this.guardedStates = {};
    this.rounds = Array(8).fill(false);
    this.abilities = {
      colorChange: [ '', '', '' ],
      guard: [ '', '', '' ],
      dupe: [ '', '', '' ]
    };
    this.saveState();
    this.closeResetModal();
  }


  getValidOptionsForState(state: string): string[] {
    const neighbors = stateAdjacencies[ state ] || [];
    const neighborVals: number[] = [];

    for (const n of neighbors) {
      const val = this.stateData[ n ];
      if (val && val !== 'X' && !this.guardedStates[ n ]) {
        const num = parseInt(val, 10);
        if (!isNaN(num)) neighborVals.push(num);
      }
    }

    if (neighborVals.length === 0) {
      return [ '1', '2', '3', '4', '5', '6' ];
    }

    let possible = new Set([ 1, 2, 3, 4, 5, 6 ]);

    for (const v of neighborVals) {
      const allowedForThisNeighbor = new Set([ v - 1, v, v + 1 ]);
      possible = new Set([ ...possible ].filter(x => allowedForThisNeighbor.has(x)));
    }

    const result = [];
    for (let i = 1; i <= 6; i++) {
      if (possible.has(i)) result.push(i.toString());
    }

    return result;
  }

  // Modal Methods
  openModal(type: 'state' | 'ability' | 'xs', key: string, index?: number) {
    if (type === 'state') {
      this.validOptions = this.getValidOptionsForState(key);
      this.isGuardChecked = !!this.guardedStates[ key ];
    } else {
      this.validOptions = [ '1', '2', '3', '4', '5', '6' ];
    }
    this.currentEditTarget = {type, key, index};
    this.isModalOpen = true;
  }

  toggleAbility(type: 'colorChange' | 'guard' | 'dupe', index: number) {
    const current = this.abilities[ type ][ index ];
    this.abilities[ type ][ index ] = current === 'X' ? '' : 'X';
    this.saveState();
  }

  toggleRound(index: number) {
    if (index >= 0 && index < this.rounds.length) {
      this.rounds[ index ] = !this.rounds[ index ];
      this.saveState();
    }
  }

  closeModal() {
    this.isModalOpen = false;
    this.currentEditTarget = null;
  }

  selectValue(value: string) {
    if (!this.currentEditTarget) return;

    const {type, key, index} = this.currentEditTarget;

    if (value === 'Clear') {
      value = '';
    }

    if (type === 'state') {
      const wasGuarded = !!this.guardedStates[ key ];
      const isNowGuarded = value !== '' ? this.isGuardChecked : false;

      this.stateData[ key ] = value;
      this.guardedStates[ key ] = isNowGuarded;

      if (wasGuarded && !isNowGuarded) {
        const lastXIndex = this.abilities.guard.lastIndexOf('X');
        if (lastXIndex !== -1) {
          this.abilities.guard[ lastXIndex ] = '';
        }
      } else if (!wasGuarded && isNowGuarded) {
        const firstEmptyIndex = this.abilities.guard.indexOf('');
        if (firstEmptyIndex !== -1) {
          this.abilities.guard[ firstEmptyIndex ] = 'X';
        }
      }
    } else if (type === 'ability' && index !== undefined) {
      (this.abilities as any)[ key ][ index ] = value;
    }

    this.saveState();
    this.closeModal();
  }
}
