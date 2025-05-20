import { HttpClient, HttpParams } from '@angular/common/http';
import { inject, Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { URLS } from '../constants/url';
import { ApiResponse, SearchParams, SearchResponse } from '../constants/search';

@Injectable({
  providedIn: 'root',
})
export class SearchService {
  _httpClient = inject(HttpClient);
  constructor() {}

  search(searchParams: SearchParams): Observable<SearchResponse> {
    let params = new HttpParams().set('query', searchParams.query);

    if (searchParams.count !== undefined) {
      params = params.set('count', searchParams.count.toString());
    }

    if (searchParams.sort_method) {
      params = params.set('sort_method', searchParams.sort_method);
    }

    if (searchParams.weight_relevance !== undefined) {
      params = params.set(
        'weight_relevance',
        searchParams.weight_relevance.toString()
      );
    }

    if (searchParams.weight_score !== undefined) {
      params = params.set('weight_score', searchParams.weight_score.toString());
    }

    if (searchParams.weight_time !== undefined) {
      params = params.set('weight_time', searchParams.weight_time.toString());
    }

    if (searchParams.use_pagerank !== undefined) {
      params = params.set('use_pagerank', searchParams.use_pagerank.toString());
    }

    return this._httpClient.get<SearchResponse>(
      `${URLS.BASE_URL}${URLS.SEARCH}`,
      { params }
    );
  }

  clearIndex(): Observable<ApiResponse> {
    return this._httpClient.delete<ApiResponse>(
      `${URLS.BASE_URL}${URLS.CLEAR_INDEXER}`
    );
  }

  triggerIndexer(): Observable<ApiResponse> {
    return this._httpClient.get<ApiResponse>(
      `${URLS.BASE_URL}${URLS.TRIGGER_INDEXER}`
    );
  }
}
