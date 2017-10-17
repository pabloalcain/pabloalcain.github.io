/* file: rectangle.c */

struct _rect {
  float height, width;
};

typedef struct _rect Rectangle;

float area(Rectangle rect) {
  return rect.height * rect.width;
}

float get_height(Rectangle rect) {
  return rect.height;
}

float get_width(Rectangle rect) {
  return rect.width;
}
