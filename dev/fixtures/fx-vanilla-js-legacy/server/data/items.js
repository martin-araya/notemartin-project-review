// server/data/items.js
// Catalogo hardcoded de productos para el endpoint correspondiente.
// El campo `premium` se usa para aplicar la clase .is-premium en el
// frontend y ocultar visualmente la opcion.
module.exports = [
  { id: 'a-001', name: 'Camiseta basica', price: 19.9,  category: 'ropa',     premium: false },
  { id: 'a-002', name: 'Pantalon clasico', price: 39.5,  category: 'ropa',     premium: false },
  { id: 'a-003', name: 'Chaqueta vintage',  price: 89.0,  category: 'ropa',     premium: true  },
  { id: 'a-004', name: 'Zapatillas runner', price: 59.0,  category: 'calzado',  premium: false },
  { id: 'a-005', name: 'Botas de cuero',   price: 129.0, category: 'calzado',  premium: true  },
  { id: 'a-006', name: 'Mochila urbana',   price: 49.0,  category: 'accesorios', premium: false },
  { id: 'a-007', name: 'Gorra deportiva',  price: 14.5,  category: 'accesorios', premium: false },
  { id: 'a-008', name: 'Reloj minimal',    price: 79.0,  category: 'accesorios', premium: true  },
  { id: 'a-009', name: 'Cinturon clasico', price: 24.0,  category: 'accesorios', premium: false },
  { id: 'a-010', name: 'Bufanda de lana',  price: 18.0,  category: 'ropa',     premium: false },
  { id: 'a-011', name: 'Guantes de piel',  price: 32.0,  category: 'accesorios', premium: true  },
  { id: 'a-012', name: 'Gafas de sol',     price: 69.0,  category: 'accesorios', premium: true  },
  { id: 'a-013', name: 'Sandalias playa',  price: 22.0,  category: 'calzado',  premium: false },
  { id: 'a-014', name: 'Polo piquet',      price: 29.0,  category: 'ropa',     premium: false },
  { id: 'a-015', name: 'Jersey de punto',  price: 55.0,  category: 'ropa',     premium: false },
  { id: 'a-016', name: 'Cazadora denim',   price: 75.0,  category: 'ropa',     premium: true  },
  { id: 'a-017', name: 'Bolsos de mano',   price: 45.0,  category: 'accesorios', premium: false },
  { id: 'a-018', name: 'Cartera clasica',  price: 38.0,  category: 'accesorios', premium: false },
  { id: 'a-019', name: 'Sneakers limited', price: 149.0, category: 'calzado',  premium: true  },
  { id: 'a-020', name: 'Camisa lino',      price: 49.0,  category: 'ropa',     premium: false }
];
