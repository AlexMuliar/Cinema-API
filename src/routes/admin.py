from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.responses import StreamingResponse

from src.core.dependencies import SessionDep
from src.models.report import get_report_for_data_range
from src.schemas.report import ReportIn
from src.utils.auth import get_current_admin_user
from src.utils.report import report_query_to_csv

admin_router = APIRouter()


@admin_router.get('/report',
                  status_code=status.HTTP_200_OK,
                  dependencies=[Depends(get_current_admin_user)],
                  )
async def generate_report(db: SessionDep, data_range: Annotated[ReportIn, Depends()]) -> StreamingResponse:
    report = await get_report_for_data_range(
        session=db,
        start_date=data_range.start_date,
        end_date=data_range.end_date,
    )
    return StreamingResponse(
        iter(report_query_to_csv(report)),
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename=report-{datetime.now}.csv"}
    )
