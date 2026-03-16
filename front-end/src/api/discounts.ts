import { ICheckout } from "../types";
import { defaultHeaders } from "./defaults";

interface IApplyDiscount {
	checkoutId: number;
	code: string;
}

export async function applyDiscount({
	checkoutId,
	code,
}: IApplyDiscount): Promise<ICheckout> {
	// TODO: implement API call to apply discount
	return Promise.resolve({} as ICheckout);
}
