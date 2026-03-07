"""
VersioningAgent - Store architecture versions in database

This rule-based agent persists architecture versions for tracking evolution.
"""

import json
import sqlite3
from datetime import datetime
from typing import Optional
from contextlib import contextmanager
from ..orchestration.state import MetaMindState, add_version_to_history
from ..utils.logging_config import AgentLogger


class VersioningAgent:
    """
    Rule-based agent that stores architecture versions.
    
    Manages:
    - Version record creation
    - Database persistence
    - Parent-child version linking
    - Metadata storage
    """
    
    def __init__(self, db_path: str = "./metamind.db"):
        """
        Initialize the VersioningAgent.
        
        Args:
            db_path: Path to SQLite database
        """
        self.db_path = db_path
        self.logger = AgentLogger("VersioningAgent")
        self._initialize_database()
    
    @contextmanager
    def _get_connection(self):
        """
        Context manager for database connections with proper cleanup.
        
        Yields:
            sqlite3.Connection: Database connection
        """
        conn = None
        try:
            conn = sqlite3.connect(self.db_path, timeout=10.0)
            conn.row_factory = sqlite3.Row
            yield conn
            conn.commit()
        except Exception as e:
            if conn:
                conn.rollback()
            self.logger.error(f"Database error: {e}")
            raise
        finally:
            if conn:
                conn.close()
    
    def _initialize_database(self):
        """Initialize database tables if they don't exist."""
        self.logger.info(f"Initializing database at {self.db_path}")
        
        conn = None
        try:
            conn = sqlite3.connect(self.db_path, timeout=10.0)
            cursor = conn.cursor()
            
            # Create runs table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS runs (
                    id TEXT PRIMARY KEY,
                    timestamp TEXT NOT NULL,
                    business_goal TEXT NOT NULL,
                    domain TEXT NOT NULL,
                    constraints_json TEXT NOT NULL,
                    weights_json TEXT NOT NULL,
                    final_architecture_id TEXT,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
            """)
            
            # Create architectures table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS architectures (
                    id TEXT PRIMARY KEY,
                    run_id TEXT NOT NULL,
                    version INTEGER NOT NULL,
                    timestamp TEXT NOT NULL,
                    architecture_json TEXT NOT NULL,
                    metrics_json TEXT NOT NULL,
                    score REAL NOT NULL,
                    changes_made TEXT,
                    parent_version INTEGER,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (run_id) REFERENCES runs(id)
                )
            """)
            
            # Create indexes
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_run_id
                ON architectures(run_id)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_version
                ON architectures(run_id, version)
            """)
            
            conn.commit()
            self.logger.info("Database initialized successfully")
        except Exception as e:
            if conn:
                conn.rollback()
            self.logger.error(f"Database initialization failed: {e}")
            raise
        finally:
            if conn:
                conn.close()
    
    def execute(self, state: MetaMindState) -> MetaMindState:
        """
        Execute version storage.
        
        Args:
            state: Current MetaMind state
            
        Returns:
            MetaMindState: Updated state
        """
        try:
            self.logger.info(f"Storing version {state['version']} for run {state['run_id']}")
            
            # Store run information
            self._store_run(state)
            
            # Store current architecture version
            self._store_architecture_version(state)
            
            # Add to iteration history in state
            selected_arch = state["selected_architecture"]
            metrics = selected_arch.get("estimated_metrics", {})
            score = selected_arch.get("final_score", 0.0)
            changes = state.get("_iteration_changes", [])
            
            state = add_version_to_history(
                state,
                selected_arch,
                metrics,
                score,
                changes
            )
            
            self.logger.info(f"Successfully stored version {state['version']}")
            print(f"✓ Stored version {state['version']} in database")
        
        except Exception as e:
            error_msg = f"VersioningAgent failed: {str(e)}"
            self.logger.error(error_msg)
            print(f"✗ {error_msg}")
            state["errors"].append(error_msg)
        
        return state
    
    def _store_run(self, state: MetaMindState):
        """
        Store run information in database.
        
        Args:
            state: Current state
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Check if run already exists
            cursor.execute("SELECT id FROM runs WHERE id = ?", (state["run_id"],))
            exists = cursor.fetchone()
            
            if not exists:
                # Insert new run
                cursor.execute("""
                INSERT INTO runs (
                    id, timestamp, business_goal, domain,
                    constraints_json, weights_json, final_architecture_id,
                    status, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                state["run_id"],
                state["timestamp"],
                state["business_goal"],
                state["domain"],
                json.dumps(state["constraints"]),
                json.dumps(state["weights"]),
                state.get("selected_architecture_id"),
                state["status"],
                datetime.utcnow().isoformat() + "Z"
            ))
            else:
                # Update existing run
                cursor.execute("""
                UPDATE runs SET
                    final_architecture_id = ?,
                    status = ?
                WHERE id = ?
            """, (
                state.get("selected_architecture_id"),
                state["status"],
                state["run_id"]
            ))
    
    def _store_architecture_version(self, state: MetaMindState):
        """
        Store architecture version in database.
        
        Args:
            state: Current state
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            selected_arch = state["selected_architecture"]
            metrics = selected_arch.get("estimated_metrics", {})
            score = selected_arch.get("final_score", 0.0)
            changes = state.get("_iteration_changes", [])
            
            # Determine parent version
            parent_version = state["version"] - 1 if state["version"] > 1 else None
            
            # Insert architecture version
            cursor.execute("""
                INSERT INTO architectures (
                    id, run_id, version, timestamp,
                    architecture_json, metrics_json, score,
                    changes_made, parent_version, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                selected_arch["architecture_id"],
                state["run_id"],
                state["version"],
                datetime.utcnow().isoformat() + "Z",
                json.dumps(selected_arch),
                json.dumps(metrics),
                score,
                json.dumps(changes),
                parent_version,
                datetime.utcnow().isoformat() + "Z"
            ))
    
    def get_run(self, run_id: str) -> Optional[dict]:
        """
        Retrieve run information.
        
        Args:
            run_id: Run ID
            
        Returns:
            dict: Run information or None
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM runs WHERE id = ?", (run_id,))
            row = cursor.fetchone()
            
            if row:
                return dict(row)
            return None
    
    def get_architecture_versions(self, run_id: str) -> list:
        """
        Retrieve all architecture versions for a run.
        
        Args:
            run_id: Run ID
            
        Returns:
            list: List of architecture versions
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM architectures
                WHERE run_id = ?
                ORDER BY version ASC
            """, (run_id,))
            
            rows = cursor.fetchall()
            
            return [dict(row) for row in rows]
    
    def get_version(self, run_id: str, version: int) -> Optional[dict]:
        """
        Retrieve specific architecture version.
        
        Args:
            run_id: Run ID
            version: Version number
            
        Returns:
            dict: Architecture version or None
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM architectures
                WHERE run_id = ? AND version = ?
            """, (run_id, version))
            
            row = cursor.fetchone()
            
            if row:
                return dict(row)
            return None
    
    def get_all_runs(self, limit: int = 50, offset: int = 0) -> list:
        """
        Retrieve all runs with pagination.
        
        Args:
            limit: Maximum number of runs to return
            offset: Number of runs to skip
            
        Returns:
            list: List of runs
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM runs
                ORDER BY created_at DESC
                LIMIT ? OFFSET ?
            """, (limit, offset))
            
            rows = cursor.fetchall()
            
            return [dict(row) for row in rows]