from fastapi import FastAPI
from app.database import Base, engine

# Import models so tables created
from app.modules.masters.uom.models import Uom
from app.modules.masters.hsn.models import Hsn
from app.modules.masters.gst_rate.models import GstRate
from app.modules.masters.tax.models import TaxMaster
from app.modules.product.models import Product
from app.modules.product_uom.models import ProductUom  # noqa

# Routers
from app.modules.masters.uom.router import router as uom_router
from app.modules.masters.hsn.router import router as hsn_router
from app.modules.masters.gst_rate.router import router as gst_router
from app.modules.masters.tax.router import router as tax_router
from app.modules.product.router import router as product_router
from app.modules.product_uom.router import router as product_uom_router
Base.metadata.create_all(bind=engine)

app = FastAPI(title="ERP Backend API")

app.include_router(uom_router)
app.include_router(hsn_router)
app.include_router(gst_router)
app.include_router(tax_router)
app.include_router(product_router)
app.include_router(product_uom_router)

@app.get("/")
def root():
    return {"message": "ERP Backend Running 🚀"}