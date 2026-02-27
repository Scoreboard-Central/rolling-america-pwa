import {Component, OnInit} from '@angular/core';
import {RouterOutlet} from '@angular/router';
import {FormsModule} from '@angular/forms';
import {CommonModule} from '@angular/common';

import {stateAdjacencies, stateNames} from './map-data';

export interface GameHistoryItem {
  id: string;
  date: string;
  xsCount: number;
  won: boolean;
  isSolo?: boolean;
  cheatsUsed?: number;
}

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [ RouterOutlet, FormsModule, CommonModule ],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent implements OnInit {
  get currentModalTitle(): string {
    if (this.currentEditTarget?.type === 'state') {
      return stateNames[ this.currentEditTarget.key ] || 'SELECT VALUE';
    }
    return 'SELECT VALUE';
  }

  title = 'rolling-america-pwa';

  // Modal State
  isModalOpen = false;
  isResetModalOpen = false;

  isSettingsModalOpen = false;
  isHistoryModalOpen = false;
  isDeleteModalOpen = false;
  isEndGameModalOpen = false;
  isRulesModalOpen = false;
  lastToggledRoundIndex: number | null = null;
  gameToDeleteId: string | null = null;

  get totalWins(): number {
    return this.groupGames.filter(g => g.won).length;
  }

  get totalLosses(): number {
    return this.groupGames.filter(g => !g.won).length;
  }

  historyTab: 'group' | 'solo' = 'group';

  get groupGames(): GameHistoryItem[] {
    return this.gameHistory.filter(g => !g.isSolo);
  }

  get soloGames(): GameHistoryItem[] {
    return this.gameHistory.filter(g => g.isSolo);
  }

  get statesMarkedCount(): number {
    return Object.values(this.stateData).filter(v => v !== '').length;
  }

  get bestSoloGame(): GameHistoryItem | null {
    if (this.soloGames.length === 0) return null;
    return this.soloGames.reduce((best, current) => {
      if (current.xsCount < best.xsCount) return current;
      if (current.xsCount === best.xsCount && (current.cheatsUsed || 0) < (best.cheatsUsed || 0)) return current;
      return best;
    });
  }

  isOverallBest(game: GameHistoryItem): boolean {
    if (!game.isSolo) return false;
    const best = this.bestSoloGame;
    return best !== null && game.xsCount === best.xsCount && (game.cheatsUsed || 0) === (best.cheatsUsed || 0);
  }

  wasBestAtTheTime(game: GameHistoryItem): boolean {
    if (!game.isSolo) return false;
    const gameIndex = this.gameHistory.indexOf(game);
    if (gameIndex === -1) return false;

    const olderGames = this.gameHistory.slice(gameIndex + 1).filter(g => g.isSolo);
    if (olderGames.length === 0) return true;

    const bestOlderScore = Math.min(...olderGames.map(g => g.xsCount));
    const bestOlderGames = olderGames.filter(g => g.xsCount === bestOlderScore);
    const bestOlderCheats = Math.min(...bestOlderGames.map(g => g.cheatsUsed || 0));

    if (game.xsCount < bestOlderScore) return true;
    if (game.xsCount === bestOlderScore && (game.cheatsUsed || 0) <= bestOlderCheats) return true;
    return false;
  }

  // Theme & History
  isDarkMode = true;
  showDiceUI = true;
  gameHistory: GameHistoryItem[] = [];

  // Intercept state
  gameWon = false;
  addToHistory = true;
  isSoloGame = false;

  currentEditTarget: {type: 'state' | 'ability' | 'xs', key: string, index?: number} | null = null;
  validOptions: string[] = [ '1', '2', '3', '4', '5', '6' ];

  readonly allDiceColors = [ 'orange', 'blue', 'purple', 'green', 'red', 'yellow', 'white' ];
  availableDice: string[] = [ ...this.allDiceColors ];
  activeDice: {color: string, value: number | null}[] = [];
  diceState: 'start' | 'selected' | 'rolled' | 'round_end' = 'start';

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

  // Dice Mechanics
  selectDice() {
    if (this.availableDice.length < 2) return;

    const selected = [];
    for (let i = 0; i < 2; i++) {
      const randIndex = Math.floor(Math.random() * this.availableDice.length);
      selected.push(this.availableDice.splice(randIndex, 1)[ 0 ]);
    }
    this.activeDice = [
      {color: selected[ 0 ], value: null},
      {color: selected[ 1 ], value: null}
    ];
    this.diceState = 'selected';
    this.saveState();
  }

  rollDice() {
    this.activeDice.forEach(die => {
      die.value = Math.floor(Math.random() * 6) + 1;
    });

    if (this.availableDice.length === 1) {
      this.diceState = 'round_end';
    } else {
      this.diceState = 'rolled';
    }
    this.saveState();
  }

  nextRound() {
    const nextUnchecked = this.rounds.findIndex(r => !r);
    if (nextUnchecked !== -1) {
      this.toggleRound(nextUnchecked);
    }
    this.availableDice = [ ...this.allDiceColors ];
    this.activeDice = [];
    this.diceState = 'start';
    this.saveState();
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
      abilities: this.abilities,
      availableDice: this.availableDice,
      activeDice: this.activeDice,
      diceState: this.diceState,
      showDiceUI: this.showDiceUI
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
      this.availableDice = parsed.availableDice || [ ...this.allDiceColors ];
      this.activeDice = parsed.activeDice || [];
      this.diceState = parsed.diceState || 'start';
      this.showDiceUI = parsed.showDiceUI !== false; // Default to true
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
    // Apply immediately to the document body
    if (this.isDarkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }

  toggleTheme() {
    this.isDarkMode = !this.isDarkMode;
    localStorage.setItem('theme', this.isDarkMode ? 'dark' : 'light');

    // Apply immediately to the document body
    if (this.isDarkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }

  toggleDiceUI() {
    this.showDiceUI = !this.showDiceUI;
    this.saveState();
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

  openRulesModal() {
    this.isRulesModalOpen = true;
  }

  closeRulesModal() {
    this.isRulesModalOpen = false;
  }

  openResetModal() {
    this.gameWon = false;
    this.addToHistory = true;
    this.isSoloGame = false;
    this.isResetModalOpen = true;
  }

  closeResetModal() {
    this.isResetModalOpen = false;
  }

  confirmReset() {
    if (this.addToHistory) {
      const cheatsUsedCount =
        this.abilities.colorChange.filter(c => c === 'X').length +
        this.abilities.guard.filter(c => c === 'X').length +
        this.abilities.dupe.filter(c => c === 'X').length;

      const newItem: GameHistoryItem = {
        id: Date.now().toString() + Math.random().toString(36).substring(2, 9),
        date: new Date().toLocaleDateString(),
        xsCount: this.xsCount,
        won: this.gameWon,
        isSolo: this.isSoloGame,
        cheatsUsed: cheatsUsedCount
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
    this.availableDice = [ ...this.allDiceColors ];
    this.activeDice = [];
    this.diceState = 'start';
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
      this.isGuardChecked = !!this.guardedStates[ key ];
      this.validOptions = this.isGuardChecked ? [ '1', '2', '3', '4', '5', '6' ] : this.getValidOptionsForState(key);
    } else {
      this.validOptions = [ '1', '2', '3', '4', '5', '6' ];
    }
    this.currentEditTarget = {type, key, index};
    this.isModalOpen = true;
  }

  onGuardToggle() {
    if (this.currentEditTarget?.type === 'state') {
      if (this.isGuardChecked) {
        // If Guard is checked, all numbers are available
        this.validOptions = [ '1', '2', '3', '4', '5', '6' ];
      } else {
        // If unchecked, recalculate based on neighbors
        this.validOptions = this.getValidOptionsForState(this.currentEditTarget.key);
      }
    }
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

      if (this.rounds.every(r => r)) {
        this.lastToggledRoundIndex = index;
        this.isEndGameModalOpen = true;
      }
    }
  }

  closeEndGameModal(confirm: boolean) {
    this.isEndGameModalOpen = false;

    if (confirm) {
      Object.keys(stateNames).forEach(stateAlias => {
        if (!this.stateData[ stateAlias ]) {
          this.stateData[ stateAlias ] = 'X';
        }
      });
      this.saveState();
    } else {
      this.rounds[ 7 ] = false;
      this.saveState();
    }
    this.lastToggledRoundIndex = null;
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
