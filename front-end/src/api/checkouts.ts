import { ICheckout } from "../types";
import { defaultHeaders } from "./defaults";

interface ICreateCheckout {
	currency: "GBP";
}

export async function createCheckout({
	currency,
}: ICreateCheckout): Promise<ICheckout> {
	const response = await window.fetch("/api/checkouts", {
		method: "POST",
		body: JSON.stringify({ currency }),
		headers: {
			...defaultHeaders,
		},
	});
	if (!response.ok) {
		const error = await response.json();
		throw new Error(error.error?.message || "Request failed");
	}
	return response.json();
}
