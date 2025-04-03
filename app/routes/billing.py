from fastapi import APIRouter, HTTPException, status, Depends
from database.database import get_session
from models.billing import *
from services.crud import billing as BillService
from typing import List

billing_route = APIRouter(tags=['Billing'])



@billing_route.get("/{id}", response_model=Bill)
async def get_bill_by_id(id: int, session=Depends(get_session)) -> Bill:
    bill = BillService.get_bill(id, session)
    if bill:
        return bill
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bill with supplied ID does not exist")


@billing_route.get("/{id}/operations", response_model=List[BillOperation])
async def get_bill_operations_list(id: int, session=Depends(get_session)) -> List[BillOperation]:
    bill_operations = BillService.get_bill_operations_list_2(id, session)
    if bill_operations:
        return bill_operations
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bill operations for supplied User ID does not exist")



@billing_route.post('/{id}/refund/{payment}')
async def bill_refund(id:int, payment:float, session=Depends(get_session)):
    if BillService.update_bill_refund(id, payment, session) is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Cannot refund bill for this User ID")

    return {"message": f"Bill for user {id} successfully refund on {payment}!"}



@billing_route.post('/{id}/refill_limits/{payment}')
async def bill_refill_limits(id:int, payment:float, session=Depends(get_session)):
    if BillService.update_bill_refill_limits(id, payment, session) is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Cannot refill limmits for this User ID")

    return {"message": f"Free day limits for user {id} successfully refund on {payment}!"}



@billing_route.post('/{id}/pay/{payment}')
async def pay(id:int, payment:float, session=Depends(get_session)):
    if BillService.pay(id, payment, session) is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Cannot make paiment for this User ID")

    return {"message": f"Pay for user {id} successfully makes on {payment}!"}
