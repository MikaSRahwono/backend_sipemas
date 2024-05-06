def get_full_image_url(request, image_field):
    if image_field:
        return request.build_absolute_uri(image_field.url)
    return None