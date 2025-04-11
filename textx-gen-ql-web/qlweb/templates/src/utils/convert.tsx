import Decimal from 'decimal.js';

export const conv_nan = (x) => isNaN(x) ? undefined : x;

export const conv_bool = (x: string | undefined): boolean | undefined => {
    return x === undefined ? undefined : x == 'true';
};
export const conv_money = (x: string | undefined): Decimal => {
    return x === undefined || x == '' ? Decimal(NaN) : Decimal(x);
}
export const conv_integer = (x: string | undefined): Decimal => {
    return conv_money(x);
}
export const str_bool = (x: boolean | undefined): string | undefined => {
    return x === undefined ? undefined : x.toString();
};
export const str_date = (x: Date | undefined): string | undefined => {
    return x === undefined ? undefined : x.toString();
};
export const str_money = (x: Decimal | undefined): string | undefined => {
    return x === undefined || x.isNaN() ? undefined : x.toString();
}
export const str_number = (x: Decimal | undefined): string | undefined => {
    return str_money(x);
}
