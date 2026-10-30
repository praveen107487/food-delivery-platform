import env from "@/config/env";

export const APP_CONFIG = {
  name: env.appName,
  description: "Discover restaurants and order your favourite food.",
  defaultPageSize: 10,
  maxPageSize: 100,
  currency: "INR",
  currencyLocale: "en-IN",
  countryCode: "IN",
  phoneCountryCode: "+91",
};

export const API_ENDPOINTS = {
  auth: {
    register: "/api/v1/auth/register",
    login: "/api/v1/auth/login",
    me: "/api/v1/auth/me",
    logout: "/api/v1/auth/logout",
  },
  restaurants: {
    list: "/api/v1/restaurants",
    search: "/api/v1/restaurants/search",
    details: (id) => `/api/v1/restaurants/${id}`,
    menu: (id) => `/api/v1/restaurants/${id}/menu-items`,
  },
  menuItems: {
    search: "/api/v1/menu-items/search",
  },
  cart: {
    get: "/api/v1/cart",
    addItem: "/api/v1/cart/items",
    updateItem: (id) => `/api/v1/cart/items/${id}`,
    removeItem: (id) => `/api/v1/cart/items/${id}`,
    clear: "/api/v1/cart",
    applyCoupon: "/api/v1/cart/coupon",
    removeCoupon: "/api/v1/cart/coupon",
  },
  coupons: {
    validate: "/api/v1/coupons/validate",
  },
  customers: {
    me: "/api/v1/customers/me",
    addresses: "/api/v1/customers/addresses",
    address: (id) => `/api/v1/customers/addresses/${id}`,
    setDefaultAddress: (id) => `/api/v1/customers/addresses/${id}/default`,
  },
  orders: {
    create: "/api/v1/orders",
    current: "/api/v1/orders/current",
    byId: (id) => `/api/v1/orders/${id}`,
    history: "/api/v1/orders/history",
  },
  payments: {
    create: "/api/v1/payments",
    byId: (id) => `/api/v1/payments/${id}`,
    verify: (id) => `/api/v1/payments/${id}/verify`,
    status: (id) => `/api/v1/payments/${id}/status`,
    retry: (id) => `/api/v1/payments/${id}/retry`,
  },
  reviews: {
    restaurants: {
      create: "/api/v1/reviews/restaurants",
      update: (id) => `/api/v1/reviews/restaurants/${id}`,
      delete: (id) => `/api/v1/reviews/restaurants/${id}`,
      list: (id) => `/api/v1/reviews/restaurants/${id}`,
      uploadImage: (id) => `/api/v1/reviews/restaurants/${id}/images`,
      listImages: (id) => `/api/v1/reviews/restaurants/${id}/images`,
      deleteImage: (id) => `/api/v1/reviews/restaurants/images/${id}`,
    },
    foodItems: {
      create: "/api/v1/reviews/food-items",
      update: (id) => `/api/v1/reviews/food-items/${id}`,
      delete: (id) => `/api/v1/reviews/food-items/${id}`,
      list: (id) => `/api/v1/reviews/food-items/${id}`,
      uploadImage: (id) => `/api/v1/reviews/food-items/${id}/images`,
      listImages: (id) => `/api/v1/reviews/food-items/${id}/images`,
      deleteImage: (id) => `/api/v1/reviews/food-items/images/${id}`,
    },
  },
  notifications: {
    list: "/api/v1/notifications",
    byId: (id) => `/api/v1/notifications/${id}`,
    markRead: (id) => `/api/v1/notifications/${id}/read`,
    markAllRead: "/api/v1/notifications/read-all",
  },
};
