import { CRS, extend, Projection, Transformation } from "leaflet";

export default new (function () {
  const unproject = function (point) {
    return this.projection.unproject({ x: point.x, y: -point.y });
  };
  const project = function (latlng) {
    return this.projection.project({ lat: -latlng.lat, lng: latlng.lng });
  };

  // For the transformation function, the new scale is 1 / 2 to the power of the max zoom
  const transformationFactor = 1 / 2 ** 8;

  const customCRS = {
    projection: Projection.LonLat,
    transformation: new Transformation(
      transformationFactor,
      0,
      -transformationFactor,
      0
    ),
    scale: function (zoom) {
      return Math.pow(2, zoom);
    },

    zoom: function (scale) {
      return Math.log(scale) / Math.LN2;
    },

    distance: function (latlng1, latlng2) {
      var dx = latlng2.lng - latlng1.lng,
        dy = latlng2.lat - latlng1.lat;

      return Math.sqrt(dx * dx + dy * dy);
    },
    infinite: true,
  };
  customCRS.toLatLng = unproject.bind(customCRS);
  customCRS.toPoint = project.bind(customCRS);

  return extend({}, CRS.Simple, customCRS);
})();
