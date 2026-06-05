from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


class CreateMapByCoord(APIView):
    # 需要用户认证才能访问此接口
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        
        
        coordinate_type = data.get('coordinate_type')
        side_length = data.get('side_length')
        email = data.get('email')
        openid = data.get('openid')
        
        if not coordinate_type or not side_length or not email:
            return Response({
                'code': 400,
                'message': '缺少必要参数'
            }, status=status.HTTP_400_BAD_REQUEST)

        if coordinate_type == 'decimal':
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            
            if not latitude or not longitude:
                return Response({
                    'code': 400,
                    'message': '十进制坐标缺少经纬度参数'
                }, status=status.HTTP_400_BAD_REQUEST)

            try:
                lat = float(latitude)
                lon = float(longitude)
                if lat < -90 or lat > 90 or lon < -180 or lon > 180:
                    return Response({
                        'code': 400,
                        'message': '经纬度超出有效范围'
                    }, status=status.HTTP_400_BAD_REQUEST)
            except ValueError:
                return Response({
                    'code': 400,
                    'message': '经纬度格式错误'
                }, status=status.HTTP_400_BAD_REQUEST)

            coord_data = {
                'type': 'decimal',
                'latitude': lat,
                'longitude': lon
            }

        elif coordinate_type == 'dms':
            lat_degree = data.get('lat_degree')
            lat_minute = data.get('lat_minute')
            lat_second = data.get('lat_second')
            lon_degree = data.get('lon_degree')
            lon_minute = data.get('lon_minute')
            lon_second = data.get('lon_second')
            
            if not all([lat_degree, lat_minute, lat_second, lon_degree, lon_minute, lon_second]):
                return Response({
                    'code': 400,
                    'message': '度分秒坐标缺少参数'
                }, status=status.HTTP_400_BAD_REQUEST)

            try:
                lat_deg = int(lat_degree)
                lat_min = int(lat_minute)
                lat_sec = float(lat_second)
                lon_deg = int(lon_degree)
                lon_min = int(lon_minute)
                lon_sec = float(lon_second)

                if lat_deg < 0 or lat_deg > 90 or lat_min < 0 or lat_min > 59 or lat_sec < 0 or lat_sec >= 60:
                    return Response({
                        'code': 400,
                        'message': '纬度度分秒超出有效范围'
                    }, status=status.HTTP_400_BAD_REQUEST)

                if lon_deg < 0 or lon_deg > 180 or lon_min < 0 or lon_min > 59 or lon_sec < 0 or lon_sec >= 60:
                    return Response({
                        'code': 400,
                        'message': '经度度分秒超出有效范围'
                    }, status=status.HTTP_400_BAD_REQUEST)
            except ValueError:
                return Response({
                    'code': 400,
                    'message': '度分秒格式错误'
                }, status=status.HTTP_400_BAD_REQUEST)

            coord_data = {
                'type': 'dms',
                'lat_degree': lat_deg,
                'lat_minute': lat_min,
                'lat_second': lat_sec,
                'lon_degree': lon_deg,
                'lon_minute': lon_min,
                'lon_second': lon_sec
            }

        else:
            return Response({
                'code': 400,
                'message': '未知的坐标格式类型'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            side = float(side_length)
            if side < 0.5 or side > 10:
                return Response({
                    'code': 400,
                    'message': '边长超出有效范围(0.5-10 km)'
                }, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({
                'code': 400,
                'message': '边长格式错误'
            }, status=status.HTTP_400_BAD_REQUEST)

        email_regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        import re
        if not re.match(email_regex, email):
            return Response({
                'code': 400,
                'message': '邮箱格式不正确'
            }, status=status.HTTP_400_BAD_REQUEST)

        print(f"地图生成请求 - 用户: {openid}, 坐标类型: {coordinate_type}, 坐标: {coord_data}, 边长: {side}km, 邮箱: {email}")

        return Response({
            'code': 0,
            'message': '地图生成请求已接收',
            'data': {
                'coordinate_type': coordinate_type,
                'coordinate': coord_data,
                'side_length': side,
                'email': email
            }
        }, status=status.HTTP_200_OK)
