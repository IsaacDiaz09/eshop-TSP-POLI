// Volt Athletics - E-commerce JS Logic
const API_BASE = '/api';

// Application State
let token = localStorage.getItem('access_token') || null;
let currentUser = null;
let cart = JSON.parse(localStorage.getItem('cart')) || [];
let products = [];
let categories = [];
let selectedProduct = null;
let selectedVariant = null;

// Filter State
let filterState = {
    search: '',
    category: '',
    brand: '',
    size: '',
    min_price: '',
    max_price: '',
    page: 1
};

// Initial Load
window.addEventListener('DOMContentLoaded', () => {
    initApp();
});

async function initApp() {
    updateAuthUI();
    await fetchCategories();
    await fetchProducts();
    renderCart();

    if (token) {
        loadUserProfile();
    }
}

// ==========================================
// API Operations
// ==========================================

// Fetch all categories
async function fetchCategories() {
    try {
        const response = await fetch(`${API_BASE}/categories/`);
        if (response.ok) {
            categories = await response.json();
            renderCategoriesFilter();
        }
    } catch (error) {
        console.error('Error fetching categories:', error);
    }
}

// Fetch products based on filters
async function fetchProducts() {
    const grid = document.getElementById('productsGrid');
    grid.innerHTML = `
        <div class="col-12 text-center my-5 w-100">
            <div class="spinner-border text-warning" role="status">
                <span class="visually-hidden">Cargando productos...</span>
            </div>
        </div>
    `;

    try {
        const queryParams = new URLSearchParams();
        if (filterState.search) queryParams.append('search', filterState.search);
        if (filterState.category) queryParams.append('category', filterState.category);
        if (filterState.brand) queryParams.append('brand', filterState.brand);
        if (filterState.size) queryParams.append('size', filterState.size);
        if (filterState.min_price) queryParams.append('min_price', filterState.min_price);
        if (filterState.max_price) queryParams.append('max_price', filterState.max_price);
        if (filterState.page) queryParams.append('page', filterState.page);

        const response = await fetch(`${API_BASE}/products/?${queryParams.toString()}`);
        if (response.ok) {
            const data = await response.json();
            products = data.results;
            renderProducts();
            renderPagination(data.count);
        }
    } catch (error) {
        console.error('Error fetching products:', error);
        grid.innerHTML = `<div class="col-12 text-center text-danger w-100 my-5"><p>Error al cargar el catálogo de productos.</p></div>`;
    }
}

// Load current user profile details
async function loadUserProfile() {
    try {
        const response = await fetch(`${API_BASE}/auth/me/`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        if (response.ok) {
            currentUser = await response.json();
            document.getElementById('usernameDisplay').textContent = currentUser.username;
            document.getElementById('authSection').classList.add('d-none');
            document.getElementById('userSection').classList.remove('d-none');
        } else {
            // Token expired or invalid
            handleLogout();
        }
    } catch (error) {
        console.error('Error loading user profile:', error);
        handleLogout();
    }
}

// ==========================================
// Authentication Event Handlers
// ==========================================

function updateAuthUI() {
    if (token) {
        document.getElementById('authSection').classList.add('d-none');
        document.getElementById('userSection').classList.remove('d-none');
    } else {
        document.getElementById('authSection').classList.remove('d-none');
        document.getElementById('userSection').classList.add('d-none');
    }
}

function setAuthTab(tab) {
    const loginTabBtn = document.getElementById('loginTab');
    const registerTabBtn = document.getElementById('registerTab');
    const loginPane = document.getElementById('loginPane');
    const registerPane = document.getElementById('registerPane');

    if (tab === 'login') {
        loginTabBtn.classList.add('active');
        registerTabBtn.classList.remove('active');
        loginPane.classList.add('show', 'active');
        registerPane.classList.remove('show', 'active');
    } else {
        loginTabBtn.classList.remove('active');
        registerTabBtn.classList.add('active');
        loginPane.classList.remove('show', 'active');
        registerPane.classList.add('show', 'active');
    }
    
    // Clear errors
    document.getElementById('loginErrorAlert').classList.add('d-none');
    document.getElementById('regErrorAlert').classList.add('d-none');
    document.getElementById('regSuccessAlert').classList.add('d-none');
}

async function handleLoginSubmit(event) {
    event.preventDefault();
    const usernameInput = document.getElementById('loginUsername');
    const passwordInput = document.getElementById('loginPassword');
    const errorAlert = document.getElementById('loginErrorAlert');

    errorAlert.classList.add('d-none');

    try {
        const response = await fetch(`${API_BASE}/auth/login/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                username: usernameInput.value,
                password: passwordInput.value
            })
        });

        const data = await response.json();

        if (response.ok) {
            token = data.access;
            localStorage.setItem('access_token', token);
            localStorage.setItem('refresh_token', data.refresh);
            
            // Clean forms
            usernameInput.value = '';
            passwordInput.value = '';

            // Close modal
            const authModal = bootstrap.Modal.getInstance(document.getElementById('authModal'));
            authModal.hide();

            // Refresh UI
            await loadUserProfile();
            renderCart(); // Hide login prompt in cart if visible
        } else {
            errorAlert.textContent = data.detail || 'Nombre de usuario o contraseña incorrectos.';
            errorAlert.classList.remove('d-none');
        }
    } catch (error) {
        console.error('Error logging in:', error);
        errorAlert.textContent = 'Ocurrió un error inesperado al iniciar sesión.';
        errorAlert.classList.remove('d-none');
    }
}

async function handleRegisterSubmit(event) {
    event.preventDefault();
    const usernameInput = document.getElementById('regUsername');
    const emailInput = document.getElementById('regEmail');
    const passwordInput = document.getElementById('regPassword');
    const errorAlert = document.getElementById('regErrorAlert');
    const successAlert = document.getElementById('regSuccessAlert');

    errorAlert.classList.add('d-none');
    successAlert.classList.add('d-none');

    try {
        const response = await fetch(`${API_BASE}/auth/register/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                username: usernameInput.value,
                email: emailInput.value,
                password: passwordInput.value
            })
        });

        const data = await response.json();

        if (response.ok) {
            successAlert.classList.remove('d-none');
            // Reset input values
            usernameInput.value = '';
            emailInput.value = '';
            passwordInput.value = '';
            // Switch to login tab after 1.5 seconds
            setTimeout(() => {
                setAuthTab('login');
            }, 1500);
        } else {
            let errorMsg = '';
            for (const key in data) {
                errorMsg += `${key}: ${data[key].join(', ')}\n`;
            }
            errorAlert.innerText = errorMsg || 'Error al registrar el usuario.';
            errorAlert.classList.remove('d-none');
        }
    } catch (error) {
        console.error('Error registering:', error);
        errorAlert.textContent = 'Ocurrió un error inesperado al registrarse.';
        errorAlert.classList.remove('d-none');
    }
}

function handleLogout(event) {
    if (event) event.preventDefault();
    token = null;
    currentUser = null;
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    
    document.getElementById('authSection').classList.remove('d-none');
    document.getElementById('userSection').classList.add('d-none');
    
    renderCart(); // Show login prompt in cart if items exist
}

// ==========================================
// Render UI Components
// ==========================================

// Render Category filter list
function renderCategoriesFilter() {
    const list = document.getElementById('categoriesFilterList');
    // Keep the "Todas" option
    list.innerHTML = `
        <div class="form-check mb-1">
            <input class="form-check-input category-filter" type="radio" name="categoryFilter" id="catAll" value="" checked onchange="handleCategoryFilterChange(this)">
            <label class="form-check-label" for="catAll">Todas las categorías</label>
        </div>
    `;

    categories.forEach(cat => {
        list.innerHTML += `
            <div class="form-check mb-1">
                <input class="form-check-input category-filter" type="radio" name="categoryFilter" id="cat_${cat.id}" value="${cat.id}" onchange="handleCategoryFilterChange(this)">
                <label class="form-check-label" for="cat_${cat.id}">${cat.name}</label>
            </div>
        `;
    });
}

function handleCategoryFilterChange(radio) {
    filterState.category = radio.value;
    applyFilters();
}

// Render Products Grid
function renderProducts() {
    const grid = document.getElementById('productsGrid');
    const countText = document.getElementById('productsCountText');

    grid.innerHTML = '';
    countText.textContent = `Mostrando ${products.length} productos`;

    if (products.length === 0) {
        grid.innerHTML = `
            <div class="col-12 text-center my-5 w-100">
                <i class="bi bi-search" style="font-size: 3rem; color: #ccc;"></i>
                <p class="mt-3 text-muted">No se encontraron productos con los filtros seleccionados.</p>
            </div>
        `;
        return;
    }

    products.forEach(product => {
        // Calculate total stock of variants
        const totalStock = product.variants.reduce((acc, variant) => acc + variant.stock, 0);
        const isOutOfStock = totalStock <= 0;

        grid.innerHTML += `
            <div class="col">
                <div class="card h-100 border product-card" onclick="viewProductDetail(${product.id})">
                    <img src="${product.image_url || 'https://via.placeholder.com/300'}" class="card-img-top object-fit-cover" alt="${product.name}" style="height: 220px;">
                    <div class="card-body d-flex flex-column">
                        <div class="d-flex justify-content-between align-items-center mb-1">
                            <span class="badge bg-secondary text-uppercase">${product.brand}</span>
                            <span class="small text-muted">${product.category.name}</span>
                        </div>
                        <h5 class="card-title fw-bold mb-2 text-dark">${product.name}</h5>
                        <p class="card-text text-muted small flex-grow-1 text-truncate">${product.description}</p>
                        
                        <div class="d-flex justify-content-between align-items-center mt-3 border-top pt-2">
                            <span class="fs-5 fw-bold text-success">COP $${product.price.toLocaleString()}</span>
                            ${isOutOfStock 
                                ? '<span class="badge bg-danger">Agotado</span>' 
                                : `<span class="badge bg-success-subtle text-success">Stock: ${totalStock}</span>`
                            }
                        </div>
                    </div>
                </div>
            </div>
        `;
    });
}

// Render Pagination Controls
function renderPagination(totalCount) {
    const nav = document.getElementById('paginationNav');
    const controls = document.getElementById('paginationControls');
    
    controls.innerHTML = '';
    
    const itemsPerPage = 9;
    const totalPages = Math.ceil(totalCount / itemsPerPage);
    
    if (totalPages <= 1) {
        nav.classList.add('d-none');
        return;
    }
    
    nav.classList.remove('d-none');
    
    const currentPage = filterState.page || 1;
    
    // Button: Previous
    const prevDisabled = currentPage === 1 ? 'disabled' : '';
    controls.innerHTML += `
        <li class="page-item ${prevDisabled}">
            <a class="page-link" href="#" onclick="changePage(event, ${currentPage - 1})">
                <span aria-hidden="true">&laquo; Anterior</span>
            </a>
        </li>
    `;
    
    // Page Numbers
    for (let i = 1; i <= totalPages; i++) {
        const activeClass = currentPage === i ? 'active' : '';
        controls.innerHTML += `
            <li class="page-item ${activeClass}">
                <a class="page-link" href="#" onclick="changePage(event, ${i})">${i}</a>
            </li>
        `;
    }
    
    // Button: Next
    const nextDisabled = currentPage === totalPages ? 'disabled' : '';
    controls.innerHTML += `
        <li class="page-item ${nextDisabled}">
            <a class="page-link" href="#" onclick="changePage(event, ${currentPage + 1})">
                <span aria-hidden="true">Siguiente &raquo;</span>
            </a>
        </li>
    `;
}

function changePage(event, pageNumber) {
    if (event) event.preventDefault();
    if (pageNumber < 1) return;
    filterState.page = pageNumber;
    fetchProducts();
    
    // Smooth scroll to catalog
    document.getElementById('catalogSection').scrollIntoView({ behavior: 'smooth' });
}

// ==========================================
// Catalog Detail Modal and Variant Logic
// ==========================================

function viewProductDetail(productId) {
    selectedProduct = products.find(p => p.id === productId);
    if (!selectedProduct) return;

    selectedVariant = null;

    const modalBody = document.getElementById('productModalBody');
    
    // Extract unique sizes and colors available
    const sizes = [...new Set(selectedProduct.variants.map(v => v.size))];
    const colors = [...new Set(selectedProduct.variants.map(v => v.color))];

    modalBody.innerHTML = `
        <div class="row">
            <div class="col-md-5 mb-3 mb-md-0">
                <img src="${selectedProduct.image_url}" alt="${selectedProduct.name}" class="img-fluid rounded border w-100 object-fit-cover" style="max-height: 380px;">
            </div>
            <div class="col-md-7">
                <span class="badge bg-secondary text-uppercase mb-2">${selectedProduct.brand}</span>
                <h2 class="fw-bold text-dark">${selectedProduct.name}</h2>
                <h3 class="text-success fw-bold mb-3">COP $${selectedProduct.price.toLocaleString()}</h3>
                
                <p class="text-secondary small border-bottom pb-3">${selectedProduct.description}</p>
                
                <!-- Variant Selector -->
                <div class="mb-3">
                    <label class="form-label fw-bold text-secondary">Color</label>
                    <div id="modalColors">
                        ${colors.map(color => `
                            <input type="radio" class="btn-check" name="modalColorRadio" id="col_${color}" value="${color}" autocomplete="off" onchange="onVariantSelectionChange()">
                            <label class="btn btn-outline-dark btn-sm me-2 mb-2" for="col_${color}">${color}</label>
                        `).join('')}
                    </div>
                </div>

                <div class="mb-4">
                    <label class="form-label fw-bold text-secondary">Talla</label>
                    <div id="modalSizes">
                        ${sizes.map(size => `
                            <input type="radio" class="btn-check" name="modalSizeRadio" id="sz_${size}" value="${size}" autocomplete="off" onchange="onVariantSelectionChange()">
                            <label class="btn btn-outline-dark btn-sm me-2 mb-2" for="sz_${size}">${size}</label>
                        `).join('')}
                    </div>
                </div>

                <!-- Stock Indicator -->
                <div class="alert alert-light border d-flex justify-content-between align-items-center mb-4 py-2 px-3">
                    <span class="text-muted"><i class="bi bi-boxes"></i> Disponibilidad:</span>
                    <span class="fw-bold text-dark" id="variantStockText">Selecciona talla y color</span>
                </div>

                <!-- Quantity Selector and Action -->
                <div class="row g-2 align-items-center">
                    <div class="col-4 col-md-3">
                        <div class="input-group">
                            <button class="btn btn-outline-secondary" type="button" onclick="decrementModalQty()">-</button>
                            <input type="text" class="form-control text-center" id="modalQtyInput" value="1" readonly>
                            <button class="btn btn-outline-secondary" type="button" onclick="incrementModalQty()">+</button>
                        </div>
                    </div>
                    <div class="col-8 col-md-9">
                        <button class="btn btn-primary w-100 py-2" id="modalAddToCartBtn" disabled onclick="addProductToCart()">
                            <i class="bi bi-cart-plus me-1"></i> Agregar al Carrito
                        </button>
                    </div>
                </div>
            </div>
        </div>
    `;

    const productModal = new bootstrap.Modal(document.getElementById('productModal'));
    productModal.show();
}

function onVariantSelectionChange() {
    const selectedColorRadio = document.querySelector('input[name="modalColorRadio"]:checked');
    const selectedSizeRadio = document.querySelector('input[name="modalSizeRadio"]:checked');
    const stockText = document.getElementById('variantStockText');
    const addToCartBtn = document.getElementById('modalAddToCartBtn');

    if (!selectedColorRadio || !selectedSizeRadio) {
        stockText.textContent = "Selecciona talla y color";
        addToCartBtn.disabled = true;
        selectedVariant = null;
        return;
    }

    const color = selectedColorRadio.value;
    const size = selectedSizeRadio.value;

    // Find the variant
    selectedVariant = selectedProduct.variants.find(v => v.size === size && v.color === color);

    if (selectedVariant) {
        if (selectedVariant.stock > 0) {
            stockText.innerHTML = `<span class="text-success"><i class="bi bi-check-circle-fill"></i> ${selectedVariant.stock} unidades disponibles</span>`;
            addToCartBtn.disabled = false;
        } else {
            stockText.innerHTML = `<span class="text-danger"><i class="bi bi-x-circle-fill"></i> Agotado en esta combinación</span>`;
            addToCartBtn.disabled = true;
        }
    } else {
        stockText.innerHTML = `<span class="text-muted"><i class="bi bi-exclamation-triangle"></i> No disponible</span>`;
        addToCartBtn.disabled = true;
    }

    // Reset qty selector to 1
    document.getElementById('modalQtyInput').value = 1;
}

function incrementModalQty() {
    const qtyInput = document.getElementById('modalQtyInput');
    let val = parseInt(qtyInput.value);
    if (selectedVariant && val < selectedVariant.stock) {
        qtyInput.value = val + 1;
    }
}

function decrementModalQty() {
    const qtyInput = document.getElementById('modalQtyInput');
    let val = parseInt(qtyInput.value);
    if (val > 1) {
        qtyInput.value = val - 1;
    }
}

// ==========================================
// Shopping Cart Operations
// ==========================================

function addProductToCart() {
    if (!selectedProduct || !selectedVariant) return;

    const qtyInput = document.getElementById('modalQtyInput');
    const qty = parseInt(qtyInput.value);

    // Check if variant already exists in cart
    const existingItem = cart.find(item => item.variantId === selectedVariant.id);
    
    if (existingItem) {
        // Check if adding exceeds stock
        if (existingItem.quantity + qty > selectedVariant.stock) {
            alert(`No puedes agregar más unidades de las disponibles. Stock total: ${selectedVariant.stock}`);
            return;
        }
        existingItem.quantity += qty;
    } else {
        cart.push({
            productId: selectedProduct.id,
            variantId: selectedVariant.id,
            name: selectedProduct.name,
            brand: selectedProduct.brand,
            size: selectedVariant.size,
            color: selectedVariant.color,
            price: selectedProduct.price,
            image_url: selectedProduct.image_url,
            availableStock: selectedVariant.stock,
            quantity: qty
        });
    }

    // Save cart
    saveCart();
    renderCart();

    // Close product modal
    const productModal = bootstrap.Modal.getInstance(document.getElementById('productModal'));
    productModal.hide();

    // Open cart offcanvas to show the product added
    const cartOffcanvas = new bootstrap.Offcanvas(document.getElementById('cartOffcanvas'));
    cartOffcanvas.show();
}

function saveCart() {
    localStorage.setItem('cart', JSON.stringify(cart));
}

function renderCart() {
    const list = document.getElementById('cartItemsList');
    const countBadge = document.getElementById('cartCountBadge');
    const totalText = document.getElementById('cartTotalText');
    const loginPrompt = document.getElementById('cartLoginPrompt');
    const checkoutBtn = document.getElementById('checkoutBtn');

    // Total quantity
    const totalQty = cart.reduce((acc, item) => acc + item.quantity, 0);
    countBadge.textContent = totalQty;

    if (cart.length === 0) {
        list.innerHTML = `
            <div class="text-center py-5 text-muted">
                <i class="bi bi-cart-x" style="font-size: 3rem;"></i>
                <p class="mt-2 mb-0">Tu carrito está vacío.</p>
                <button class="btn btn-sm btn-outline-warning mt-2" data-bs-dismiss="offcanvas">Seguir explorando</button>
            </div>
        `;
        totalText.textContent = "COP $0";
        loginPrompt.classList.add('d-none');
        checkoutBtn.disabled = true;
        return;
    }

    checkoutBtn.disabled = false;
    list.innerHTML = '';
    let totalPrice = 0;

    cart.forEach((item, index) => {
        const itemTotal = item.price * item.quantity;
        totalPrice += itemTotal;

        list.innerHTML += `
            <div class="card mb-3 border bg-light">
                <div class="card-body p-3">
                    <div class="row g-2 align-items-center">
                        <div class="col-3">
                            <img src="${item.image_url}" alt="${item.name}" class="img-fluid rounded object-fit-cover" style="height: 65px; width: 65px;">
                        </div>
                        <div class="col-9">
                            <div class="d-flex justify-content-between mb-1">
                                <span class="fw-bold text-dark text-truncate d-block" style="max-width: 180px;">${item.name}</span>
                                <button class="btn btn-sm text-danger p-0" onclick="removeCartItem(${index})"><i class="bi bi-trash"></i></button>
                            </div>
                            <div class="small text-muted mb-2">
                                <span class="badge bg-secondary-subtle text-dark me-1">Talla: ${item.size}</span>
                                <span class="badge bg-secondary-subtle text-dark">Color: ${item.color}</span>
                            </div>
                            <div class="d-flex justify-content-between align-items-center">
                                <div class="input-group input-group-sm" style="width: 90px;">
                                    <button class="btn btn-outline-secondary btn-sm" onclick="updateCartQty(${index}, -1)">-</button>
                                    <input type="text" class="form-control text-center py-0" value="${item.quantity}" readonly>
                                    <button class="btn btn-outline-secondary btn-sm" onclick="updateCartQty(${index}, 1)">+</button>
                                </div>
                                <span class="fw-bold text-success small">COP $${itemTotal.toLocaleString()}</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    });

    totalText.textContent = `COP $${totalPrice.toLocaleString()}`;

    // Login check
    if (token) {
        loginPrompt.classList.add('d-none');
    } else {
        loginPrompt.classList.remove('d-none');
    }
}

function updateCartQty(index, dir) {
    const item = cart[index];
    if (dir === 1) {
        if (item.quantity < item.availableStock) {
            item.quantity += 1;
        } else {
            alert(`No hay suficiente stock. Límite disponible: ${item.availableStock}`);
        }
    } else {
        if (item.quantity > 1) {
            item.quantity -= 1;
        } else {
            removeCartItem(index);
            return;
        }
    }
    saveCart();
    renderCart();
}

function removeCartItem(index) {
    cart.splice(index, 1);
    saveCart();
    renderCart();
}

function openAuthModalFromCart(event) {
    event.preventDefault();
    // Close offcanvas
    const cartOffcanvas = bootstrap.Offcanvas.getInstance(document.getElementById('cartOffcanvas'));
    cartOffcanvas.hide();
    
    // Open auth modal
    const authModal = new bootstrap.Modal(document.getElementById('authModal'));
    authModal.show();
    setAuthTab('login');
}

// Checkout submission
async function handleCheckout() {
    const errorAlert = document.getElementById('checkoutErrorAlert');
    errorAlert.classList.add('d-none');

    if (!token) {
        // Trigger Login Prompt
        const cartOffcanvas = bootstrap.Offcanvas.getInstance(document.getElementById('cartOffcanvas'));
        cartOffcanvas.hide();
        const authModal = new bootstrap.Modal(document.getElementById('authModal'));
        authModal.show();
        setAuthTab('login');
        return;
    }

    // Format items for API
    const itemsPayload = cart.map(item => ({
        variant_id: item.variantId,
        quantity: item.quantity
    }));

    try {
        const response = await fetch(`${API_BASE}/orders/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                items: itemsPayload
            })
        });

        const data = await response.json();

        if (response.ok) {
            // Close Cart offcanvas
            const cartOffcanvas = bootstrap.Offcanvas.getInstance(document.getElementById('cartOffcanvas'));
            cartOffcanvas.hide();

            // Clear Cart state
            cart = [];
            saveCart();
            renderCart();

            // Open Confirmation modal
            document.getElementById('successOrderId').textContent = `#${data.id}`;
            document.getElementById('successOrderTotal').textContent = `COP $${data.total_price.toLocaleString()}`;
            
            const successModal = new bootstrap.Modal(document.getElementById('successOrderModal'));
            successModal.show();

            // Refresh products catalog in the background to show new stock numbers
            await fetchProducts();
        } else {
            let errorText = "Error al completar la orden.";
            if (data.non_field_errors) {
                errorText = data.non_field_errors.join(', ');
            } else if (typeof data === 'object') {
                errorText = Object.values(data).flat().join(', ');
            }
            errorAlert.textContent = errorText;
            errorAlert.classList.remove('d-none');
        }
    } catch (error) {
        console.error('Error in checkout:', error);
        errorAlert.textContent = 'Ocurrió un error inesperado al procesar tu compra.';
        errorAlert.classList.remove('d-none');
    }
}

// ==========================================
// History of Orders (My Orders Modal)
// ==========================================

async function loadMyOrders() {
    const modalBody = document.getElementById('ordersModalBody');
    modalBody.innerHTML = `
        <div class="text-center py-5">
            <div class="spinner-border text-warning" role="status">
                <span class="visually-hidden">Cargando pedidos...</span>
            </div>
        </div>
    `;

    try {
        const response = await fetch(`${API_BASE}/orders/`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (response.ok) {
            const orders = await response.json();
            
            if (orders.length === 0) {
                modalBody.innerHTML = `
                    <div class="text-center py-5 text-muted">
                        <i class="bi bi-bag-x" style="font-size: 3rem;"></i>
                        <p class="mt-2">No has realizado ningún pedido aún.</p>
                    </div>
                `;
                return;
            }

            modalBody.innerHTML = orders.map(order => `
                <div class="card mb-3 border bg-light">
                    <div class="card-header bg-light text-dark d-flex justify-content-between align-items-center py-2 border-bottom">
                        <span class="fw-bold">Pedido #${order.id}</span>
                        <span class="small">${new Date(order.created_at).toLocaleDateString('es-CO', { hour: '2-digit', minute: '2-digit' })}</span>
                    </div>
                    <div class="card-body p-3">
                        <div class="table-responsive">
                            <table class="table table-sm table-borderless mb-2">
                                <thead>
                                    <tr class="text-secondary small">
                                        <th>Artículo</th>
                                        <th>Variante</th>
                                        <th class="text-center">Cant.</th>
                                        <th class="text-end">Precio unit.</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    ${order.items.map(item => `
                                        <tr class="align-middle">
                                            <td><span class="fw-semibold">${item.brand}</span> ${item.product_name}</td>
                                            <td>Talla: ${item.size} | Color: ${item.color}</td>
                                            <td class="text-center">${item.quantity}</td>
                                            <td class="text-end">COP $${item.price.toLocaleString()}</td>
                                        </tr>
                                    `).join('')}
                                </tbody>
                            </table>
                        </div>
                        <div class="border-top pt-2 d-flex justify-content-between align-items-center">
                            <span class="badge bg-success">${order.status_display}</span>
                            <span class="fw-bold text-success fs-5">Total: COP $${order.total_price.toLocaleString()}</span>
                        </div>
                    </div>
                </div>
            `).join('');

        } else {
            modalBody.innerHTML = `<div class="alert alert-danger">Error al cargar el historial de pedidos.</div>`;
        }
    } catch (error) {
        console.error('Error loading orders:', error);
        modalBody.innerHTML = `<div class="alert alert-danger">Error de conexión al cargar pedidos.</div>`;
    }
}

// ==========================================
// Search & Filter Operations
// ==========================================

function handleBasicSearch(event) {
    event.preventDefault();
    const searchInput = document.getElementById('searchInput');
    filterState.search = searchInput.value.trim();
    filterState.page = 1; // Reset to page 1
    fetchProducts();
}

function applyFilters() {
    const brandSelect = document.getElementById('brandFilter');
    const minPriceInput = document.getElementById('minPriceInput');
    const maxPriceInput = document.getElementById('maxPriceInput');
    const selectedSizeRadio = document.querySelector('input[name="sizeFilter"]:checked');

    filterState.brand = brandSelect.value;
    filterState.min_price = minPriceInput.value;
    filterState.max_price = maxPriceInput.value;
    filterState.size = selectedSizeRadio ? selectedSizeRadio.value : '';
    filterState.page = 1; // Reset to page 1

    fetchProducts();
}

function clearFilters() {
    // Reset Form Controls
    document.getElementById('brandFilter').value = '';
    document.getElementById('minPriceInput').value = '';
    document.getElementById('maxPriceInput').value = '';
    document.getElementById('searchInput').value = '';
    
    // Reset Size Radio
    document.getElementById('sizeAll').checked = true;

    // Reset Category Radio
    const catAllRadio = document.getElementById('catAll');
    if (catAllRadio) catAllRadio.checked = true;

    // Reset State
    filterState = {
        search: '',
        category: '',
        brand: '',
        size: '',
        min_price: '',
        max_price: '',
        page: 1 // Reset to page 1
    };

    fetchProducts();
}

function resetCatalog(event) {
    if (event) event.preventDefault();
    clearFilters();
}
