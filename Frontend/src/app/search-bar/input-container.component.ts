import {
  AfterViewInit,
  Component,
  ElementRef,
  EventEmitter,
  OnInit,
  Output,
  ViewChild,
} from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { SearchService } from '../services/search.service';
import {
  SearchResponse,
  SearchResultItem,
  SortMethod,
} from '../constants/search';
import { MessageService } from 'primeng/api';
import { finalize } from 'rxjs';

// PrimeNG Imports
import { ToastModule } from 'primeng/toast';
import { ButtonModule } from 'primeng/button';
import { DropdownModule } from 'primeng/dropdown';
import { CardModule } from 'primeng/card';
import { ProgressSpinnerModule } from 'primeng/progressspinner';
import { DividerModule } from 'primeng/divider';
import { InputSwitchModule } from 'primeng/inputswitch';
import { InputTextModule } from 'primeng/inputtext';
import { SliderModule } from 'primeng/slider';
import { OverlayPanelModule } from 'primeng/overlaypanel';
import { TooltipModule } from 'primeng/tooltip';

@Component({
  selector: 'app-input-container',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    // PrimeNG Modules
    ProgressSpinnerModule,
    InputTextModule,
    ButtonModule,
    CardModule,
    DividerModule,
    DropdownModule,
    ToastModule,
    OverlayPanelModule,
    InputSwitchModule,
    InputTextModule,
    SliderModule,
    TooltipModule,
  ],
  providers: [MessageService],
  templateUrl: './input-container.component.html',
  styleUrl: './input-container.component.scss',
})
export class InputContainerComponent implements OnInit {
  @ViewChild('messageInput') messageInput!: ElementRef<HTMLTextAreaElement>;
  @Output() resultsFetched = new EventEmitter<SearchResultItem[]>();

  public userInput = '';
  public searchResults: SearchResultItem[] = [];
  public isLoading = false;
  public sortOptions = [
    { label: 'Relevance', value: SortMethod.RELEVANCE },
    { label: 'Score', value: SortMethod.SCORE },
    { label: 'Time', value: SortMethod.TIME },
  ];
  public selectedSortMethod = SortMethod.RELEVANCE;
  public usePageRank = true;
  public count = 10;
  public weightRelevance = 1;
  public weightScore = 1;
  public weightTime = 1;

  constructor(
    private searchService: SearchService,
    private messageService: MessageService
  ) {}

  ngOnInit(): void {
    // Initialize component
  }

  onInput(): void {
    // Adjust textarea height as content changes
    const textarea = this.messageInput?.nativeElement;
    if (textarea) {
      textarea.style.height = 'auto';
      textarea.style.height = `${textarea.scrollHeight}px`;
    }
  }

  onKeyDown(event: KeyboardEvent): void {
    if (
      event.key === 'Enter' &&
      !event.shiftKey &&
      this.userInput.trim() !== ''
    ) {
      event.preventDefault();
      this.onSendMessage();
    }
  }

  onSendMessage(): void {
    const query = this.userInput.trim();
    if (!query) return;

    this.isLoading = true;
    this.searchResults = [];

    this.searchService
      .search({
        query,
        count: this.count,
        sort_method: this.selectedSortMethod,
        weight_relevance: this.weightRelevance,
        weight_score: this.weightScore,
        weight_time: this.weightTime,
        use_pagerank: this.usePageRank,
      })
      .pipe(finalize(() => (this.isLoading = false)))
      .subscribe({
        next: (response: SearchResponse) => {
          this.searchResults = response.data;
          this.resultsFetched.emit(response.data);
          this.messageService.add({
            severity: 'success',
            summary: 'Success',
            detail: `${response.message}`,
          });
        },
        error: (error) => {
          console.error('Search error:', error);
          this.messageService.add({
            severity: 'error',
            summary: 'Error',
            detail: 'Failed to fetch search results. Please try again.',
          });
        },
      });
  }

  triggerIndexer(): void {
    this.isLoading = true;
    this.searchService
      .triggerIndexer()
      .pipe(finalize(() => (this.isLoading = false)))
      .subscribe({
        next: (response) => {
          this.messageService.add({
            severity: 'success',
            summary: 'Success',
            detail: response.message,
          });
        },
        error: (error) => {
          console.error('Indexer error:', error);
          this.messageService.add({
            severity: 'error',
            summary: 'Error',
            detail: 'Failed to trigger indexer. Please try again.',
          });
        },
      });
  }

  clearIndex(): void {
    this.isLoading = true;
    this.searchService
      .clearIndex()
      .pipe(finalize(() => (this.isLoading = false)))
      .subscribe({
        next: (response) => {
          this.searchResults = [];
          this.resultsFetched.emit([]);
          this.messageService.add({
            severity: 'success',
            summary: 'Success',
            detail: response.message,
          });
        },
        error: (error) => {
          console.error('Clear index error:', error);
          this.messageService.add({
            severity: 'error',
            summary: 'Error',
            detail: 'Failed to clear index. Please try again.',
          });
        },
      });
  }
}
