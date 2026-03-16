import { useReducer } from "react";
import checkoutReducer, {
	ICheckoutReducer,
	ICheckoutState,
} from "../reducers/checkout-reducer";
import CheckoutSummary from "../components/organisms/CheckoutSummary/CheckoutSummary";
import CheckoutTotals from "../components/organisms/CheckoutTotals/CheckoutTotals";
import Discount from "../components/molecules/Discount/Discount";
import Button from "../components/atoms/Button";
import { formatPrice } from "../utils/money";
import { initialiseCheckout } from "../services/initialise-checkout";

export interface ICheckoutPageProps {
	title: string;
}

export default function Checkout({ title }: ICheckoutPageProps) {
	const initialCheckoutState: ICheckoutState = {
		checkout: {
			id: 0,
			currency: "GBP",
			items: [],
			sub_total: 0,
			total: 0,
			discount_code: null,
			discount_amount: 0,
		},
	};

	const [{ checkout }, dispatch] = useReducer<ICheckoutReducer>(
		checkoutReducer,
		initialCheckoutState
	);

	return (
		<div>
			{title ? <h1>{title}</h1> : null}
			<div>
				<h2>Simulate a checkout</h2>
				<Button
					label="Create a new checkout"
					onClick={async () => {
						try {
							const checkout = await initialiseCheckout({ currency: "GBP" });
							dispatch({ type: "INITIALISE_CHECKOUT", checkout });
						} catch (err) {
							console.error(err);
						}
					}}
				/>
			</div>
			<div>
				<CheckoutSummary
					title="Your order"
					items={checkout.items}
					currency={checkout.currency}
					dispatch={dispatch}
				/>
				<Discount />
				<CheckoutTotals
					title="Order total"
					totals={[
						{
							label: "Sub-total",
							amount: formatPrice({
								amount: checkout.sub_total,
								currency: checkout.currency,
							}),
						},
						{
							label: "Discount total",
							amount: formatPrice({ amount: checkout.discount_amount, currency: checkout.currency }),
						},
						{
							label: "Total",
							amount: formatPrice({
								amount: checkout.total,
								currency: checkout.currency,
							}),
						},
					]}
				/>
				<Button label="Place Order" onClick={() => console.log(checkout)} />
			</div>
		</div>
	);
}
