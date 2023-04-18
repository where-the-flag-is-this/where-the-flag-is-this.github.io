type properties = {
    "flag": string;
    "geoshape": string;
    "countryLabel": string;
    "population":string;
    "area": string;
}

export type Place = {
    type: string;
    properties: properties;
    geometry: any
};