import { defaultHeaders } from "./defaults";
import { ICheckout } from "../types";

interface ICreateCheckoutItem {
	checkoutId: number;
	productId: number;
	quantity: number;
}

interface IUpdateCheckoutItem {
	checkoutItemId: number;
	quantity: number;
}

export async function createCheckoutItem({
	checkoutId,
	productId,
	quantity,
}: ICreateCheckoutItem): Promise<ICheckout> {
	const response = await window.fetch("/api/checkout_items", {
		method: "POST",
		headers: {
			...defaultHeaders,
		},
		body: JSON.stringify({
			checkout_id: checkoutId,
			product_id: productId,
			quantity,
		}),
	});
	if (!response.ok) {
		const error = await response.json();
		throw new Error(error.error?.message || "Request failed");
	}
	return response.json();
}

export async function updateCheckoutItem({
	checkoutItemId,
	quantity,
}: IUpdateCheckoutItem): Promise<ICheckout> {
	const response = await window.fetch(
		`/api/checkout_items/${checkoutItemId}`,
		{
			method: "PUT",
			headers: {
				...defaultHeaders,
			},
			body: JSON.stringify({
				quantity,
			}),
		}
	);
	if (!response.ok) {
		const error = await response.json();
		throw new Error(error.error?.message || "Request failed");
	}
	return response.json();
}
