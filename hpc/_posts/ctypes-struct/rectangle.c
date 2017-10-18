/* file: rectangle.c */

struct _rect {
  float height, width;
};

typedef struct _rect Rectangle;

float area(Rectangle rect) {
  return rect.height * rect.width;
}
