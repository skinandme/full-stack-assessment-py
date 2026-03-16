export interface IProduct {
	id: number;
	sku: string;
	name: string;
	unit_price: number;
}

export interface ICheckoutItem {
	id: number;
	product: IProduct;
	quantity: number;
	sub_total: number;
}

export interface ICheckout {
	id: number;
	currency: "GBP";
	items: ICheckoutItem[];
	sub_total: number;
	total: number;
	discount_code: string | null;
	discount_amount: number;
}
