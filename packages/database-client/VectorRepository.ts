import { Pool } from 'pg';

export class VectorRepository {
  /** Raw SQL integration for high-performance HNSW search (1536D) */
  private static readonly DEFAULT_LIMIT = 5;
  
  constructor(private pool: Pool) {}

  async findSimilarAgents(queryVector: number[], limit: number = VectorRepository.DEFAULT_LIMIT) {
    const vectorStr = `[${queryVector.join(',')}]`;
    // Operator <=> to Cosine Distance w pgvector
    return this.pool.query(
      'SELECT id, 1 - (embedding <=> $1) as ARI_Sim FROM agents ORDER BY embedding <=> $1 LIMIT $2',
      [vectorStr, limit]
    );
  }
}
