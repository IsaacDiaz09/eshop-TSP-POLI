import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from api.models import Category, Product, ProductVariant

class Command(BaseCommand):
    help = 'Seeds the database with categories, 50 products, variants, and an admin user'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting database seed...')

        # 1. Create superuser if it doesn't exist
        if not User.objects.filter(username='admin').exists():
            self.stdout.write('Creating superuser...')
            User.objects.create_superuser('admin', 'admin@volt.com', 'adminpassword')
            self.stdout.write('Superuser created: admin / adminpassword')
        else:
            self.stdout.write('Superuser admin already exists')

        # 2. Check if products exist
        if Product.objects.exists():
            self.stdout.write('Database already contains products. Removing old products to re-seed...')
            Product.objects.all().delete()
            Category.objects.all().delete()

        # 3. Create Categories
        self.stdout.write('Creating categories...')
        categories_data = [
            {'name': 'Calzado', 'slug': 'calzado'},
            {'name': 'Ropa Superior', 'slug': 'ropa-superior'},
            {'name': 'Ropa Inferior', 'slug': 'ropa-inferior'},
            {'name': 'Accesorios', 'slug': 'accesorios'},
        ]
        
        categories = {}
        for cat_data in categories_data:
            cat, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={'name': cat_data['name']}
            )
            categories[cat_data['slug']] = cat

        # 4. Define 50 Products Data (20 original + 30 new variety items)
        products_data = [
            # Category: Calzado (10 items total)
            {
                'name': 'Volt Runner X1',
                'brand': 'Volt',
                'category': categories['calzado'],
                'price': 120000.00,
                'description': 'Tenis de running ultraligeros con amortiguación premium de espuma reactiva. Ideales para largas distancias sobre asfalto.',
                'image_url': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=600&auto=format&fit=crop&q=80'
            },
            {
                'name': 'Apex Trailblazer',
                'brand': 'Apex',
                'category': categories['calzado'],
                'price': 145000.00,
                'description': 'Tenis de trail running todo terreno con suela dentada de alto agarre y membrana impermeable transpirable.',
                'image_url': 'https://images.unsplash.com/photo-1539185441755-769473a23570?w=600&auto=format&fit=crop&q=80'
            },
            {
                'name': 'Nebula Court Pro',
                'brand': 'Nebula',
                'category': categories['calzado'],
                'price': 160000.00,
                'description': 'Calzado de alto rendimiento para baloncesto y tenis. Ofrece máxima estabilidad en los tobillos y soporte lateral.',
                'image_url': 'https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa?w=600&auto=format&fit=crop&q=80'
            },
            {
                'name': 'Stryker Cleats',
                'brand': 'Stryker',
                'category': categories['calzado'],
                'price': 180000.00,
                'description': 'Guayos de fútbol profesional con capellada de cuero sintético texturizado para un control excepcional del balón.',
                'image_url': 'https://images.unsplash.com/photo-1511886929837-354d827aae26?w=600&auto=format&fit=crop&q=80'
            },
            {
                'name': 'Aero Comfort Slip-On',
                'brand': 'Aero',
                'category': categories['calzado'],
                'price': 95000.00,
                'description': 'Tenis deportivos slip-on de malla elástica. Flexibles y sumamente cómodos para caminatas diarias.',
                'image_url': 'https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?w=600&auto=format&fit=crop&q=80'
            },
            # 5 New Calzado items
            {
                'name': 'Volt Golf Max',
                'brand': 'Volt',
                'category': categories['calzado'],
                'price': 165000.00,
                'description': 'Zapatos de golf de cuero premium con tacos híbridos para tracción en el césped.',
                'image_url': 'https://images.unsplash.com/photo-1535131749006-b7f58c99034b?w=600&auto=format&fit=crop&q=80'
            },
            {
                'name': 'Apex Tour Cycling',
                'brand': 'Apex',
                'category': categories['calzado'],
                'price': 185000.00,
                'description': 'Zapatillas de ciclismo de ruta con suela rígida de carbono y ajuste milimétrico de dial.',
                'image_url': 'https://images.unsplash.com/photo-1517649763962-0c623066013b?w=600&auto=format&fit=crop&q=80'
            },
            {
                'name': 'Nebula Lift Force',
                'brand': 'Nebula',
                'category': categories['calzado'],
                'price': 155000.00,
                'description': 'Calzado plano para levantamiento de pesas con correa de empeine ancha para estabilidad.',
                'image_url': 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?w=600&auto=format&fit=crop&q=80'
            },
            {
                'name': 'Stryker Track Spike',
                'brand': 'Stryker',
                'category': categories['calzado'],
                'price': 135000.00,
                'description': 'Zapatillas de atletismo con clavos intercambiables para tracción explosiva en pista.',
                'image_url': 'https://images.unsplash.com/photo-1476480862126-209bfaa8edc8?w=600&auto=format&fit=crop&q=80'
            },
            {
                'name': 'Aero Ridge Hiker',
                'brand': 'Aero',
                'category': categories['calzado'],
                'price': 175000.00,
                'description': 'Botas de montaña de caña media con suela Vibram y refuerzos protectores contra rocas.',
                'image_url': 'https://images.unsplash.com/photo-1520639888713-7851133b1ed0?w=600&auto=format&fit=crop&q=80'
            },

            # Category: Ropa Superior (15 items total)
            {
                'name': 'DryFit Alpha Tee',
                'brand': 'Volt',
                'category': categories['ropa-superior'],
                'price': 45000.00,
                'description': 'Camiseta deportiva de microfibra de poliéster. Tecnología de absorción de sudor para mantenerte seco y fresco.',
                'image_url': 'https://images.unsplash.com/photo-1581655353564-df123a1eb820?w=600&auto=format&fit=crop&q=80'
            },
            {
                'name': 'Thermoshield Hoodie',
                'brand': 'Apex',
                'category': categories['ropa-superior'],
                'price': 85000.00,
                'description': 'Saco con capucha y forro térmico. Tejido flexible que retiene el calor corporal ideal para entrenar al aire libre en climas fríos.',
                'image_url': 'https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=600&auto=format&fit=crop&q=80'
            },
            {
                'name': 'Aero-Breeze Singlet',
                'brand': 'Aero',
                'category': categories['ropa-superior'],
                'price': 38000.00,
                'description': 'Esqueleto de running ultraligero y de espalda nadadora. Paneles de malla transpirable para ventilación máxima.',
                'image_url': 'https://images.unsplash.com/photo-1508962914676-134849a727f0?w=600&auto=format&fit=crop&q=80'
            },
            {
                'name': 'Compression Matrix Longsleeve',
                'brand': 'Nebula',
                'category': categories['ropa-superior'],
                'price': 65000.00,
                'description': 'Camiseta de compresión de manga larga. Mejora el flujo sanguíneo y el soporte muscular durante entrenamientos intensos.',
                'image_url': 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?w=600&auto=format&fit=crop&q=80'
            },
            {
                'name': 'Veloce Windbreaker',
                'brand': 'Volt',
                'category': categories['ropa-superior'],
                'price': 110000.00,
                'description': 'Chaqueta cortavientos ultraligera e impermeable con detalles reflectivos para visibilidad nocturna durante el running.',
                'image_url': 'https://images.unsplash.com/photo-1548883354-7622d03aca27?w=600&auto=format&fit=crop&q=80'
            },
            # 10 New Ropa Superior items
            {
                'name': 'PowerHold Sports Bra',
                'brand': 'Nebula',
                'category': categories['ropa-superior'],
                'price': 48000.00,
                'description': 'Top deportivo de alto soporte con copas moldeadas y espalda cruzada ajustable.',
                'image_url': 'https://images.unsplash.com/photo-1518310383802-640c2de311b2?w=600&auto=format&fit=crop&q=80'
            },
            {
                'name': 'Thermoshield Insulated Vest',
                'brand': 'Apex',
                'category': categories['ropa-superior'],
                'price': 78000.00,
                'description': 'Chaleco deportivo acojinado con aislamiento sintético ligero y repelencia al viento.',
                'image_url': 'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=600&auto=format&fit=crop&q=80'
            },
            {
                'name': 'Veloce Quarter-Zip',
                'brand': 'Volt',
                'category': categories['ropa-superior'],
                'price': 58000.00,
                'description': 'Camiseta de manga larga con cremallera corta en el pecho y cuello semi-alto para climas frescos.',
                'image_url': 'https://images.unsplash.com/photo-1518611012118-696072aa579a?w=600&auto=format&fit=crop&q=80'
            },
            {
                'name': 'Stryker Soccer Jersey',
                'brand': 'Stryker',
                'category': categories['ropa-superior'],
                'price': 62000.00,
                'description': 'Camiseta oficial de fútbol con tecnología de secado rápido y corte atlético transpirable.',
                'image_url': 'https://images.unsplash.com/photo-1508098682722-e99c43a406b2?w=600&auto=format&fit=crop&q=80'
            },
            {
                'name': 'Nebula Hoops Jersey',
                'brand': 'Nebula',
                'category': categories['ropa-superior'],
                'price': 54000.00,
                'description': 'Camiseta de baloncesto sin mangas, confeccionada en malla holgada ultra-ventilada.',
                'image_url': 'https://images.unsplash.com/photo-1546519638-68e109498ffc?w=600&auto=format&fit=crop&q=80'
            },
            {
                'name': 'Aero UV Rashguard',
                'brand': 'Aero',
                'category': categories['ropa-superior'],
                'price': 49000.00,
                'description': 'Camiseta de natación de manga larga con protección solar certificada UPF 50+.',
                'image_url': 'https://images.unsplash.com/photo-1530541930197-ff16ac917b0e?w=600&auto=format&fit=crop&q=80'
            },
            {
                'name': 'ZenFlow Yoga Tank',
                'brand': 'Volt',
                'category': categories['ropa-superior'],
                'price': 35000.00,
                'description': 'Camiseta de tirantes holgada, confeccionada con una mezcla de algodón ultra-suave.',
                'image_url': 'https://images.unsplash.com/photo-1506126613408-eca07ce68773?w=600&auto=format&fit=crop&q=80'
            },
            {
                'name': 'Alpine Fleece Jacket',
                'brand': 'Apex',
                'category': categories['ropa-superior'],
                'price': 92000.00,
                'description': 'Chaqueta de vellón polar térmico de alta montaña con cremallera completa y bolsillos de seguridad.',
                'image_url': 'https://images.unsplash.com/photo-1578587018452-892bacefd3f2?w=600&auto=format&fit=crop&q=80'
            },
            {
                'name': 'Aero Peloton Jersey',
                'brand': 'Aero',
                'category': categories['ropa-superior'],
                'price': 72000.00,
                'description': 'Jersey de ciclismo profesional con ajuste aerodinámico y 3 bolsillos de acceso trasero.',
                'image_url': 'https://images.unsplash.com/photo-1485965120184-e220f721d03e?w=600&auto=format&fit=crop&q=80'
            },
            {
                'name': 'Volt Muscle Tank',
                'brand': 'Volt',
                'category': categories['ropa-superior'],
                'price': 32000.00,
                'description': 'Camiseta de tirantes anchos con sisa caída. Ajuste holgado ideal para entrenamientos de fuerza.',
                'image_url': 'https://images.unsplash.com/photo-1583454110551-21f2fa2afe61?w=600&auto=format&fit=crop&q=80'
            },

            # Category: Ropa Inferior (13 items total)
            {
                'name': 'Apex Joggers',
                'brand': 'Apex',
                'category': categories['ropa-inferior'],
                'price': 75000.00,
                'description': 'Pantalones tipo jogger con ajuste cónico. Algodón y poliéster elástico de tacto suave con bolsillos con cremallera.',
                'image_url': 'https://images.unsplash.com/photo-1552346154-21d32810aba3?w=600&auto=format&fit=crop&q=80'
            },
            {
                'name': 'Flex-Stretch Shorts',
                'brand': 'Volt',
                'category': categories['ropa-inferior'],
                'price': 42000.00,
                'description': 'Pantaloneta de entrenamiento con aberturas laterales para total libertad de movimiento. Incluye licra interior de compresión ligera.',
                'image_url': 'https://images.unsplash.com/photo-1539185441755-769473a23570?w=600&auto=format&fit=crop&q=80'
            },
            {
                'name': 'PowerHold Leggings',
                'brand': 'Nebula',
                'category': categories['ropa-inferior'],
                'price': 80000.00,
                'description': 'Licras deportivas de pretina alta para mujer. Tejido grueso a prueba de sentadillas con soporte compresivo de alta duración.',
                'image_url': 'https://images.unsplash.com/photo-1506152983158-b4a74a01c721?w=600&auto=format&fit=crop&q=80'
            },
            {
                'name': 'Aero-Vent Track Pants',
                'brand': 'Aero',
                'category': categories['ropa-inferior'],
                'price': 90000.00,
                'description': 'Pantalones de sudadera deportivos de corte clásico. Botones de presión laterales para quitar y poner fácilmente sobre el calzado.',
                'image_url': 'https://images.unsplash.com/photo-1476480862126-209bfaa8edc8?w=600&auto=format&fit=crop&q=80'
            },
            {
                'name': 'Compression Fit Shorts',
                'brand': 'Stryker',
                'category': categories['ropa-inferior'],
                'price': 48000.00,
                'description': 'Shorts de compresión masculinos de secado rápido. Reducen la fricción e inician soporte muscular clave en cuádriceps.',
                'image_url': 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?w=600&auto=format&fit=crop&q=80'
            },
            # 8 New Ropa Inferior items
            {
                'name': 'ZenFlow Yoga Pants',
                'brand': 'Volt',
                'category': categories['ropa-inferior'],
                'price': 78000.00,
                'description': 'Pantalones de yoga de corte bota ligeramente ancha con pretina alta ultra-cómoda.',
                'image_url': 'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=600&auto=format&fit=crop&q=80'
            },
            {
                'name': 'Alpine Cargo Pants',
                'brand': 'Apex',
                'category': categories['ropa-inferior'],
                'price': 115000.00,
                'description': 'Pantalones cargo de montaña de tejido ripstop, convertibles a shorts mediante cremallera.',
                'image_url': 'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=600&auto=format&fit=crop&q=80'
            },
            {
                'name': 'PowerHold Running Tights',
                'brand': 'Nebula',
                'category': categories['ropa-inferior'],
                'price': 88000.00,
                'description': 'Licras largas de compresión con paneles reflectivos y bolsillo lateral para celular.',
                'image_url': 'https://images.unsplash.com/photo-1476480862126-209bfaa8edc8?w=600&auto=format&fit=crop&q=80'
            },
            {
                'name': 'Stryker Swim Trunks',
                'brand': 'Stryker',
                'category': categories['ropa-inferior'],
                'price': 46000.00,
                'description': 'Pantaloneta de natación de secado rápido con forro interior de malla suave.',
                'image_url': 'https://images.unsplash.com/photo-1530541930197-ff16ac917b0e?w=600&auto=format&fit=crop&q=80'
            },
            {
                'name': 'Aero Tennis Skirt',
                'brand': 'Aero',
                'category': categories['ropa-inferior'],
                'price': 52000.00,
                'description': 'Falda deportiva con short interno de compresión y bolsillo integrado para pelotas.',
                'image_url': 'https://images.unsplash.com/photo-1587280501635-68a0e82cd5ff?w=600&auto=format&fit=crop&q=80'
            },
            {
                'name': 'Aero Peloton Bib Shorts',
                'brand': 'Aero',
                'category': categories['ropa-inferior'],
                'price': 95000.00,
                'description': 'Pantaloneta de ciclismo profesional con cargaderas elásticas de malla y badana ergonómica.',
                'image_url': 'https://images.unsplash.com/photo-1485965120184-e220f721d03e?w=600&auto=format&fit=crop&q=80'
            },
            {
                'name': 'Volt Athletic Sweatpants',
                'brand': 'Volt',
                'category': categories['ropa-inferior'],
                'price': 68000.00,
                'description': 'Pantalones de sudadera deportivos, de corte suelto clásico y tacto afelpado interno.',
                'image_url': 'https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=600&auto=format&fit=crop&q=80'
            },
            {
                'name': 'Volt Green Golf Trousers',
                'brand': 'Volt',
                'category': categories['ropa-inferior'],
                'price': 98000.00,
                'description': 'Pantalón clásico de golf con tejido elástico hidrófugo de alto rendimiento.',
                'image_url': 'https://images.unsplash.com/photo-1535131749006-b7f58c99034b?w=600&auto=format&fit=crop&q=80'
            },

            # Category: Accesorios (12 items total)
            {
                'name': 'Hydration Pro Backpack',
                'brand': 'Apex',
                'category': categories['accesorios'],
                'price': 130000.00,
                'description': 'Maleta de hidratación con bolsa de agua de 2 litros incorporada. Correas ergonómicas y ajuste de pecho para running/ciclismo.',
                'image_url': 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=600&auto=format&fit=crop&q=80'
            },
            {
                'name': 'AeroGrip Gym Gloves',
                'brand': 'Aero',
                'category': categories['accesorios'],
                'price': 35000.00,
                'description': 'Guantes de levantamiento de pesas acolchados con muñequera ajustable para protección antideslizante y soporte articular.',
                'image_url': 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?w=600&auto=format&fit=crop&q=80'
            },
            {
                'name': 'Thermo-Strap Smartband',
                'brand': 'Nebula',
                'category': categories['accesorios'],
                'price': 190000.00,
                'description': 'Banda inteligente de monitoreo de actividad. Mide ritmo cardíaco, pasos, calorías consumidas y calidad de sueño.',
                'image_url': 'https://images.unsplash.com/photo-1575311373937-040b8e1fd5b6?w=600&auto=format&fit=crop&q=80'
            },
            {
                'name': 'Volt Cushion Socks (3-pack)',
                'brand': 'Volt',
                'category': categories['accesorios'],
                'price': 25000.00,
                'description': 'Paquete de 3 pares de medias deportivas tobilleras. Soporte de arco reforzado y talón acolchado anti-ampollas.',
                'image_url': 'https://images.unsplash.com/photo-1582966772680-860e372bb558?w=600&auto=format&fit=crop&q=80'
            },
            {
                'name': 'Apex Grip Headband',
                'brand': 'Apex',
                'category': categories['accesorios'],
                'price': 18000.00,
                'description': 'Banda elástica absorbente para el sudor con tira de silicona interior antideslizante.',
                'image_url': 'https://images.unsplash.com/photo-1518310383802-640c2de311b2?w=600&auto=format&fit=crop&q=80'
            },
            # 7 New Accesorios items
            {
                'name': 'Volt Duffel Bag 40L',
                'brand': 'Volt',
                'category': categories['accesorios'],
                'price': 90000.00,
                'description': 'Maleta deportiva de 40L con compartimento separado y ventilado para tenis.',
                'image_url': 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=600&auto=format&fit=crop&q=80'
            },
            {
                'name': 'ZenFlow Eco Yoga Mat',
                'brand': 'Volt',
                'category': categories['accesorios'],
                'price': 75000.00,
                'description': 'Tapete de yoga ecológico TPE de 6mm de espesor, antideslizante con correa elástica.',
                'image_url': 'https://images.unsplash.com/photo-1592432678016-e910b452f9a2?w=600&auto=format&fit=crop&q=80'
            },
            {
                'name': 'Stryker Steel Flask 1L',
                'brand': 'Stryker',
                'category': categories['accesorios'],
                'price': 42000.00,
                'description': 'Termo de acero inoxidable con doble pared al vacío. Mantiene el frío por 24 horas.',
                'image_url': 'https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=600&auto=format&fit=crop&q=80'
            },
            {
                'name': 'Aero Run Belt',
                'brand': 'Aero',
                'category': categories['accesorios'],
                'price': 28000.00,
                'description': 'Cinturón elástico ultraligero con bolsillos impermeables y salida para audífonos.',
                'image_url': 'https://images.unsplash.com/photo-1476480862126-209bfaa8edc8?w=600&auto=format&fit=crop&q=80'
            },
            {
                'name': 'Nebula Knee Sleeves (Pair)',
                'brand': 'Nebula',
                'category': categories['accesorios'],
                'price': 62000.00,
                'description': 'Par de rodilleras de neopreno de 7mm para soporte de articulaciones durante levantamientos.',
                'image_url': 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?w=600&auto=format&fit=crop&q=80'
            },
            {
                'name': 'Stryker Sports Cap',
                'brand': 'Stryker',
                'category': categories['accesorios'],
                'price': 22000.00,
                'description': 'Gorra de visera curva ligera con paneles laterales cortados con láser para ventilación.',
                'image_url': 'https://images.unsplash.com/photo-1588850561407-ed78c282e89b?w=600&auto=format&fit=crop&q=80'
            },
            {
                'name': 'Aero Goggles Pro',
                'brand': 'Aero',
                'category': categories['accesorios'],
                'price': 39000.00,
                'description': 'Gafas profesionales de natación hidrodinámicas con lentes espejados y protección UV.',
                'image_url': 'https://images.unsplash.com/photo-1530541930197-ff16ac917b0e?w=600&auto=format&fit=crop&q=80'
            },
        ]

        # 5. Populate products and variants
        sizes = ['S', 'M', 'L', 'XL']
        colors = ['Negro', 'Gris', 'Azul']

        self.stdout.write('Inserting products and variants...')
        for prod_data in products_data:
            product = Product.objects.create(
                name=prod_data['name'],
                brand=prod_data['brand'],
                category=prod_data['category'],
                price=prod_data['price'],
                description=prod_data['description'],
                image_url=prod_data['image_url']
            )
            
            # Create variants: S, M, L, XL for Negro and Gris (at least 8 variants per product)
            for color in colors[:2]:  # Negro and Gris
                for size in sizes:
                    ProductVariant.objects.create(
                        product=product,
                        size=size,
                        color=color,
                        stock=random.randint(5, 15)
                    )

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded database with {len(products_data)} items, variants and categories.'))
