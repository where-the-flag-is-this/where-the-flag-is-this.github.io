type properties = {
    "flag": string;
    "geoshape": string;
    "countryLabel": string;
}

export type Place = {
    type: string;
    properties: properties;
    geometry: any
};