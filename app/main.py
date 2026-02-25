from fastapi import FastAPI
from app.database import Base, engine

# ✅ Import models so Base.metadata.create_all() creates tables
from app.modules.sales.models import sales_invoice  # noqa
from app.modules.product.models import product, product_price, product_unit, product_tax  # noqa

# ✅ Import routers
from app.modules.sales.routers.sales_invoice_router import router as sales_invoice_router
from app.modules.product.routers.product_router import router as product_router

# ✅ Create tables (for dev only; in production use Alembic)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="ERP Backend API")

# ✅ Register routes
app.include_router(sales_invoice_router)
app.include_router(product_router)

@app.get("/")
def root():
    return {"message": "ERP Backend Running 🚀"}