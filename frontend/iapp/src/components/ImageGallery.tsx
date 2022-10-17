import React from 'react';
import "react-image-gallery/styles/css/image-gallery.css";
import * as ReactImageGallery from 'react-image-gallery';


export type ImgData = {
  original: string,
  thumbnail: string,
}

interface Props {
  images: ImgData[],
  width?: number | string,
  height?: number | string,
};

const ImageGallery: React.FC<Props> = (props: Props) => {
  return (
    <div style={{width: props.width ? props.width : 600, height: props.height ? props.height : 400, margin: "0 auto",}}>
    <ReactImageGallery.default items={props.images as any} />
    </div>
  )
}

export default ImageGallery;
