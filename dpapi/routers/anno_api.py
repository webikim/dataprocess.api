import os
import json
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse

from dpapi import image_path, label_path, out_path
from dpapi.schema.anno_api import Anno, AnnoMeta

FILE_EXCEPTION = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="File not found",
    headers={"WWW-Authenticate": "Bearer"},
)

router = APIRouter(prefix='/annoapi')


@router.get('/anno/get')
async def anno_get(path: str, name: str):
    try:
        out_dir = os.path.join(out_path, path)
        with open(os.path.join(out_dir, name + '.json'), 'r') as f:
            anno = json.load(f)
            if 'path' in anno.keys():
                del anno['path']
            if 'name' in anno.keys():
                del anno['name']
            return anno
    except Exception:
        pass
    raise FILE_EXCEPTION


@router.delete('/anno/delete')
def anno_delete(param: AnnoMeta):
    out_dir = os.path.join(out_path, param.path)
    os.remove(os.path.join(out_dir, param.name + '.json'))
    return 'OK'


# FIXME refine schema for param, when data structure from front is fixed
@router.post('/anno/save')
def anno_save(param: Anno):
    param.data['path'] = param.path
    param.data['name'] = param.name
    if 'bbox_show' in param.data.keys():
        del param.data['bbox_show']
    if 'bbox_update' in param.data.keys():
        del param.data['bbox_update']
    out_dir = os.path.join(out_path, param.path)
    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)
    with open(os.path.join(out_dir, param.name + '.json'), 'w') as f:
        f.write(json.dumps(param.data))
        f.close()
    return 'OK'


@router.get('/dir/list')
async def list_dir():
    full_list = os.listdir(image_path)
    dir_list = [name for name in full_list if os.path.isdir(os.path.join(image_path, name))]
    return dir_list


@router.get('/file/list')
async def file_dir(path: str):
    full_list = os.listdir(os.path.join(image_path, path))
    file_list = [name for name in full_list if not os.path.isdir(os.path.join(image_path, name))]
    img_list = [name for name in file_list if name.find('.') > 0 and name.split('.')[1] == 'jpg']
    return img_list


# FIXME change return file to link to file or CDN when publish into real server
@router.get('/img/get')
def image_get(path: str, name: str):
    file_path = os.path.join(os.path.join(image_path, path), name)
    if os.path.exists(file_path):
        response = FileResponse(file_path, media_type='image/jpeg')
        response.headers['Content-Disposition'] = 'attachment; filename=' + name
        return response
    raise FILE_EXCEPTION


@router.get('/label/get')
def label_get(path: str, name: str):
    if path is not None and name is not None:
        label_dir = os.path.join(label_path, path)
        filename = name
        parts = filename.split('.')
        if len(parts) > 1:
            filename = parts[0]
        try:
            with open(os.path.join(label_dir, filename + '.json'), 'r', encoding='utf8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error occurred - ", e)
    return {}
