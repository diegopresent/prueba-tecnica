from .categories import router 
from .products import router 
from .images import router 

from .categories import (
    create_category,
    delete_category,
    read_categories,
    read_category,
    update_category,
)

from .products import (
    create_product,
    delete_product,
    read_product,
    read_products,
    update_product,
)

from .images import (
    create_image,
    delete_image,
    read_image,
    read_images
)

