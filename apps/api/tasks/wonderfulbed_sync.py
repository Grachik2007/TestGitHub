"""
Celery tasks for Wonderfulbed parser sync
Запускается ежедневно в 0:00 MSK
"""
import logging
from datetime import datetime
from celery import shared_task
from agents.wonderfulbed_parser import run_parser

logger = logging.getLogger(__name__)


@shared_task
def sync_wonderfulbed_daily():
    """
    Ежедневная синхронизация товаров с wonderfulbed.ru
    Запускается в 0:00 MSK
    """
    logger.info("🚀 Starting daily Wonderfulbed sync task...")

    try:
        import asyncio

        result = asyncio.run(run_parser())

        if result.get("success"):
            logger.info(
                f"✅ Sync successful! "
                f"Products: {result.get('products_synced')}, "
                f"Duration: {result.get('duration_seconds')}s"
            )

            # Log to database
            from models import SyncLog

            SyncLog.create(
                agent_type="wonderfulbed_parser",
                status="success",
                products_count=result.get("products_synced"),
                feed_file=result.get("feed_file"),
                duration_seconds=result.get("duration_seconds"),
                metadata=result,
            )
        else:
            logger.error(f"❌ Sync failed: {result.get('error')}")

            SyncLog.create(
                agent_type="wonderfulbed_parser",
                status="failed",
                error_message=result.get("error"),
            )

        return result

    except Exception as e:
        logger.error(f"❌ Task error: {e}", exc_info=True)
        return {"success": False, "error": str(e)}


@shared_task
def sync_wonderfulbed_manual(force: bool = False):
    """
    Ручная синхронизация товаров (по требованию)
    """
    logger.info(f"👤 Manual Wonderfulbed sync triggered (force={force})")

    try:
        import asyncio

        result = asyncio.run(run_parser())
        return result

    except Exception as e:
        logger.error(f"❌ Manual sync error: {e}")
        return {"success": False, "error": str(e)}


@shared_task
def check_sync_status():
    """Проверка статуса последней синхронизации"""
    try:
        from models import SyncLog

        last_sync = SyncLog.query.filter_by(
            agent_type="wonderfulbed_parser"
        ).order_by(SyncLog.created_at.desc()).first()

        if last_sync:
            return {
                "last_sync": last_sync.created_at.isoformat(),
                "status": last_sync.status,
                "products_count": last_sync.products_count,
            }
        return {"last_sync": None, "status": "never"}

    except Exception as e:
        logger.error(f"Error checking sync status: {e}")
        return {"error": str(e)}
