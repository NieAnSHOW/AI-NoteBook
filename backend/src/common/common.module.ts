import { Module, Global } from '@nestjs/common';
import { CommonService } from './common.service';
import { PrismaService } from './prisma.service';

@Global()
@Module({
  providers: [CommonService, PrismaService],
  exports: [CommonService, PrismaService],
})
export class CommonModule {}
