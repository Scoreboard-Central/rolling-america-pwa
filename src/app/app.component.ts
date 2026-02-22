import {Component, OnInit} from '@angular/core';
import {RouterOutlet} from '@angular/router';
import {FormsModule} from '@angular/forms';
import {CommonModule} from '@angular/common';

import {stateAdjacencies} from './map-data';

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

  openResetModal() {
    this.isResetModalOpen = true;
  }

  closeResetModal() {
    this.isResetModalOpen = false;
  }

  confirmReset() {
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
