import { createCheckout } from "../api/checkouts";
import { createCheckoutItem } from "../api/checkout-items";

export async function initialiseCheckout({ currency }: { currency: "GBP" }) {
	const checkout = await createCheckout({ currency });
	return createCheckoutItem({
		checkoutId: checkout.id,
		productId: 1,
		quantity: 1,
	});
}
